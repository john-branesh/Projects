import readline from 'readline';

console.log ("MPD Analyzer Started...");

const r1 = readline.createInterface({
    input: process.stdin,
    output: process.stdout
})

r1.question("Enter the path to the MPD file: ", (filepath)=>{
    console.log(`MPD file path: ${filepath}`);

    r1.close();
})