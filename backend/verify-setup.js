const http = require('http');

console.log('Starting Backend Service verification...\n');

// Wait for server to start
setTimeout(() => {
  // Test 1: Health endpoint
  console.log('Test 1: Testing health endpoint...');
  http.get('http://localhost:3000/health', (res) => {
    let data = '';
    res.on('data', (chunk) => { data += chunk; });
    res.on('end', () => {
      const response = JSON.parse(data);
      if (res.statusCode === 200 && response.success) {
        console.log('✓ Health endpoint working correctly');
        console.log(`  Response: ${JSON.stringify(response)}\n`);
      } else {
        console.log('✗ Health endpoint failed');
      }

      // Test 2: 404 handling
      console.log('Test 2: Testing 404 error handling...');
      http.get('http://localhost:3000/nonexistent', (res) => {
        let data = '';
        res.on('data', (chunk) => { data += chunk; });
        res.on('end', () => {
          if (res.statusCode === 404) {
            console.log('✓ 404 error handling working correctly');
            console.log(`  Status: ${res.statusCode}\n`);
          } else {
            console.log('✗ 404 error handling failed');
          }

          // Test 3: CORS headers
          console.log('Test 3: Testing CORS headers...');
          if (res.headers['access-control-allow-origin']) {
            console.log('✓ CORS headers present');
            console.log(`  Origin: ${res.headers['access-control-allow-origin']}\n`);
          } else {
            console.log('✗ CORS headers missing\n');
          }

          console.log('Verification complete!');
          process.exit(0);
        });
      }).on('error', (err) => {
        console.log('✗ Error:', err.message);
        process.exit(1);
      });
    });
  }).on('error', (err) => {
    console.log('✗ Error:', err.message);
    console.log('Make sure the server is running with: npm start');
    process.exit(1);
  });
}, 2000);
