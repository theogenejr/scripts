const fs = require("fs");

function modifySRTTimestamps(inputFilePath, secondsToAdd) {
  fs.readFile(inputFilePath, "utf8", (err, data) => {
    if (err) {
      console.error("Error reading file:", err);
      return;
    }

    // Split the content by new lines to process each subtitle block separately
    const lines = data.split("\n");
    let modifiedContent = "";

    for (let i = 0; i < lines.length; i++) {
      let line = lines[i];

      // Check if the line is a timestamp line
      if (
        line.match(
          /(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})/
        )
      ) {
        const timestampRegex =
          /(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})/;
        const matches = line.match(timestampRegex);

        // Extract hours, minutes, seconds, and milliseconds from the timestamp
        let hours1 = parseInt(matches[1]);
        let minutes1 = parseInt(matches[2]);
        let seconds1 = parseInt(matches[3]);
        let milliseconds1 = parseInt(matches[4]);
        let hours2 = parseInt(matches[5]);
        let minutes2 = parseInt(matches[6]);
        let seconds2 = parseInt(matches[7]);
        let milliseconds2 = parseInt(matches[8]);

        // Convert timestamps to milliseconds
        let timestamp1 =
          hours1 * 3600000 + minutes1 * 60000 + seconds1 * 1000 + milliseconds1;
        let timestamp2 =
          hours2 * 3600000 + minutes2 * 60000 + seconds2 * 1000 + milliseconds2;

        // Add the specified number of seconds
        timestamp1 += secondsToAdd * 1000;
        timestamp2 += secondsToAdd * 1000;

        // Convert milliseconds back to hours, minutes, seconds, and milliseconds
        hours1 = Math.floor(timestamp1 / 3600000);
        timestamp1 %= 3600000;
        minutes1 = Math.floor(timestamp1 / 60000);
        timestamp1 %= 60000;
        seconds1 = Math.floor(timestamp1 / 1000);
        milliseconds1 = timestamp1 % 1000;

        hours2 = Math.floor(timestamp2 / 3600000);
        timestamp2 %= 3600000;
        minutes2 = Math.floor(timestamp2 / 60000);
        timestamp2 %= 60000;
        seconds2 = Math.floor(timestamp2 / 1000);
        milliseconds2 = timestamp2 % 1000;

        // Format the modified timestamps
        const modifiedTimestamp1 = `${hours1
          .toString()
          .padStart(2, "0")}:${minutes1.toString().padStart(2, "0")}:${seconds1
          .toString()
          .padStart(2, "0")},${milliseconds1.toString().padStart(3, "0")}`;
        const modifiedTimestamp2 = `${hours2
          .toString()
          .padStart(2, "0")}:${minutes2.toString().padStart(2, "0")}:${seconds2
          .toString()
          .padStart(2, "0")},${milliseconds2.toString().padStart(3, "0")}`;

        // Replace the original timestamps with modified ones
        line = line.replace(
          timestampRegex,
          `${modifiedTimestamp1} --> ${modifiedTimestamp2}`
        );
      }

      // Append the modified line to the content
      modifiedContent += line + "\n";
    }

    // Write the modified content to a new file
    const outputFilePath = inputFilePath.replace(".srt", "_modified.srt");
    fs.writeFile(outputFilePath, modifiedContent, "utf8", (err) => {
      if (err) {
        console.error("Error writing file:", err);
        return;
      }
      console.log(`Modified SRT file has been saved to ${outputFilePath}`);
    });
  });
}

// Example usage:
const inputFilePath = "badrinath.srt"; // Provide the location of the input SRT file
const secondsToAdd = -5.5; // Specify the number of seconds to add to timestamps
modifySRTTimestamps(inputFilePath, secondsToAdd);
