# SRT Timestamp Modifier

A Node.js script that modifies timestamps in SRT (SubRip Subtitle) files. This
tool allows you to adjust subtitle timing by adding or subtracting seconds from
all timestamps in an SRT file.

## Features

- Modify all subtitle timestamps in an SRT file
- Support for both positive and negative time adjustments
- Maintains original SRT file format and structure
- Preserves millisecond precision
- Creates a new file instead of modifying the original
- Handles hours, minutes, seconds, and milliseconds correctly

## Prerequisites

- Node.js (version 12.0.0 or higher)
- A text editor
- SRT files to modify

## Installation

1. Create a new directory for your project:

```bash
mkdir srt-modifier
cd srt-modifier
```

2. Save the script as `srtModifier.js`

3. Make sure you have read/write permissions in the directory

## Usage

### Basic Usage

```javascript
const inputFilePath = "path/to/your/subtitle.srt";
const secondsToAdd = 2.5; // Positive number to delay subtitles
modifySRTTimestamps(inputFilePath, secondsToAdd);
```

### Command Line Usage

1. Create a new file (e.g., `adjust.js`):

```javascript
const inputFile = process.argv[2];
const seconds = parseFloat(process.argv[3]);

if (!inputFile || isNaN(seconds)) {
  console.error("Usage: node adjust.js <input-file> <seconds>");
  process.exit(1);
}

modifySRTTimestamps(inputFile, seconds);
```

2. Run from command line:

```bash
node adjust.js mysubtitle.srt 2.5
```

## Time Adjustment Examples

1. Delay subtitles by 2.5 seconds:

```javascript
modifySRTTimestamps("movie.srt", 2.5);
```

2. Make subtitles appear 1.5 seconds earlier:

```javascript
modifySRTTimestamps("movie.srt", -1.5);
```

3. Adjust by milliseconds:

```javascript
modifySRTTimestamps("movie.srt", 0.5); // 500ms delay
```

## Input File Format

The script expects standard SRT format:

```
1
00:00:20,000 --> 00:00:22,000
First subtitle text

2
00:00:22,500 --> 00:00:24,500
Second subtitle text
```

## Output

- Creates a new file with "\_modified" suffix
- Example: `movie.srt` → `movie_modified.srt`
- Preserves original file
- Maintains original formatting

## Error Handling

The script handles common errors:

- File reading errors
- Invalid SRT format
- File writing permissions
- Invalid time adjustments

## Limitations

- Only processes .srt files
- Doesn't validate subtitle text content
- No support for other subtitle formats (e.g., .sub, .ass)
- Large time adjustments might result in negative timestamps

## Troubleshooting

1. **File Not Found Error**:

   - Check if the file path is correct
   - Ensure you have read permissions

2. **Permission Denied**:

   - Check write permissions in output directory
   - Run with appropriate user privileges

3. **Invalid Timestamps**:
   - Verify input file is properly formatted
   - Check for corrupted SRT files

## Common Use Cases

1. **Sync Correction**:

   ```javascript
   // Fix subtitles that are 2 seconds late
   modifySRTTimestamps("movie.srt", -2);
   ```

2. **Batch Processing**:
   ```javascript
   const files = ["ep1.srt", "ep2.srt", "ep3.srt"];
   files.forEach((file) => modifySRTTimestamps(file, 1.5));
   ```

## Best Practices

1. Always backup original SRT files
2. Test with small segments first
3. Verify output with a video player
4. Use precise decimal values for fine-tuning

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Built for the Node.js ecosystem
- Inspired by the need for precise subtitle synchronization
