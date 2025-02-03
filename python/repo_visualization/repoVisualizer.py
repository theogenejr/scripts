import requests
import graphviz
from github import Github
from github.GithubException import GithubException, UnknownObjectException, BadCredentialsException
from pathlib import Path
from urllib.parse import urlparse

def verify_token(token):
    """
    Verifies GitHub token and prints available scopes
    """
    try:
        g = Github(token)
        user = g.get_user()
        # Try to access user data to verify authentication
        user.login
        # Get token scopes
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.get('https://api.github.com/user', headers=headers)
        scopes = response.headers.get('X-OAuth-Scopes', '').split(', ')
        print(f"Token verified. Available scopes: {scopes}")
        return True
    except BadCredentialsException:
        print("Invalid token or token has been revoked")
        return False
    except Exception as e:
        print(f"Error verifying token: {str(e)}")
        return False

def extract_repo_info(repo_url):
    """
    Extracts repository owner and name from various GitHub URL formats.
    """
    try:
        # Handle both HTTPS and SSH URLs
        if repo_url.startswith('git@'):
            # SSH format: git@github.com:owner/repo.git
            path = repo_url.split(':', 1)[1]
        else:
            # HTTPS format: https://github.com/owner/repo
            parsed = urlparse(repo_url)
            path = parsed.path.lstrip('/')
        
        # Remove .git extension if present
        if path.endswith('.git'):
            path = path[:-4]
            
        # Split into owner and repo
        owner, repo = path.split('/')
        return owner, repo
    except Exception:
        return None

def visualize_github_repo(repo_url, access_token=None, output_file="repo_structure", debug=True):
    """
    Creates a visual representation of a GitHub repository structure.
    """
    if debug:
        print(f"\nDebug Information:")
        print(f"Repository URL: {repo_url}")
        print(f"Token provided: {'Yes' if access_token else 'No'}")

    # Validate and extract repository information
    repo_info = extract_repo_info(repo_url)
    if not repo_info:
        raise ValueError("Invalid GitHub repository URL format")
    
    owner, repo_name = repo_info
    full_repo_name = f"{owner}/{repo_name}"
    
    if debug:
        print(f"Owner: {owner}")
        print(f"Repository: {repo_name}")
    
    # Verify token if provided
    if access_token and debug:
        verify_token(access_token)
    
    # Initialize GitHub connection
    g = Github(access_token) if access_token else Github()
    
    try:
        # Test API rate limit first
        if debug:
            rate_limit = g.get_rate_limit()
            print(f"API Rate Limit: {rate_limit.core.remaining}/{rate_limit.core.limit}")
        
        # Get repository
        repo = g.get_repo(full_repo_name)
        
        # Verify repository access
        try:
            repo.get_contents("")
        except UnknownObjectException:
            raise ValueError(
                f"Repository '{full_repo_name}' not found. Please verify:\n"
                "1. The repository exists\n"
                "2. Your access token has the 'repo' scope for private repositories\n"
                "3. You have access to this repository in your GitHub account\n"
                "4. The repository name is correct (case-sensitive)"
            )
        except Exception as e:
            if "404" in str(e):
                raise ValueError(
                    f"Access denied to repository '{full_repo_name}'. Please verify:\n"
                    "1. The token has sufficient permissions (needs 'repo' scope)\n"
                    "2. You are a collaborator on this repository\n"
                    "3. The organization allows your token access (check organization settings)"
                )
            raise

        # Create visualization
        dot = graphviz.Digraph(comment='Repository Structure')
        dot.attr(rankdir='LR')
        dot.attr('node', shape='box', style='rounded')
        
        def add_contents(path, parent=None):
            try:
                contents = repo.get_contents(path)
                
                if not isinstance(contents, list):
                    contents = [contents]
                    
                for content in contents:
                    if content.name.startswith('.'):
                        continue
                        
                    node_name = content.path.replace('/', '_')
                    
                    if content.type == 'dir':
                        dot.node(node_name, content.name + '/', style='filled', fillcolor='lightblue')
                    else:
                        dot.node(node_name, content.name)
                    
                    if parent:
                        dot.edge(parent.replace('/', '_'), node_name)
                    
                    if content.type == 'dir':
                        add_contents(content.path, content.path)
                        
            except Exception as e:
                print(f"Error processing {path}: {str(e)}")
        
        # Start visualization from root
        add_contents("")
        
        # Save the visualization
        try:
            dot.render(output_file, view=True, format='png')
            print(f"\nVisualization saved as {output_file}.png")
        except Exception as e:
            print(f"Error saving visualization: {str(e)}")
            
    except Exception as e:
        raise Exception(f"Error accessing repository: {str(e)}")

# Example usage
if __name__ == "__main__":
    REPO_URL = "REPOSITORY_URL"
    # TOKEN = "ACCESS_TOKEN"  # Optional
    
    
    try:
        visualize_github_repo(
            repo_url=REPO_URL,
            # access_token=TOKEN, # Optional
            output_file="repo_visualization",
            debug=True  # Set to True to see detailed debug information
        )
    except Exception as e:
        print(f"\nError: {str(e)}")