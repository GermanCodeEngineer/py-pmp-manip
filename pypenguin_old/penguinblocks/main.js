import { parse } from "./syntax.js";
import * as fs from "fs";

// Get command-line arguments
const args = process.argv.slice(2); // Ignore "node" and script name
// Use arguments to determine input code or file
if (args.length < 2) {
  console.error("Usage: node main.js <inputPath> <outputPath>");
  process.exit(1);
}

const inputPath = args[0]; // First argument is the  input path
const outputPath = args[1]; // Second argument is the output file path
const code = fs.readFileSync(inputPath, 'utf8')

// Parse the code and write to the output file
const doc = parse(code, {});
fs.writeFileSync(outputPath, JSON.stringify(doc));
