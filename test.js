const fs = require('fs');


const filepath = './test.json';
let i = 0;

if (fs.existsSync(filepath)) {
    i = JSON.parse(fs.readFileSync(filepath).toString());
}

if (i === 5) {
    fs.writeFileSync('BUILD_DONE.txt', "1");
    process.exit(0)
}

i++;

fs.writeFileSync(filepath, JSON.stringify(i));
fs.writeFileSync('RESULT_MESSAGE.txt', `Step ${i}/5 done`);

process.exit(0)