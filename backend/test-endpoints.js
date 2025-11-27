const axios = require('axios');

const BASE_URL = 'http://localhost:3000';

async function testEndpoints() {
  console.log('Testing Backend API Endpoints...\n');

  try {
    // Test 1: POST /api/profile - Create profile
    console.log('1. Testing POST /api/profile...');
    const profileData = {
      income: 75000,
      spending_score: 65,
      saving_frequency: 7,
      loan_behavior: 2
    };
    const profileResponse = await axios.post(`${BASE_URL}/api/profile`, profileData);
    console.log('✓ Profile created:', profileResponse.data);
    const userId = profileResponse.data.data.id;
    console.log('');

    // Test 2: GET /api/user/:id - Get profile
    console.log('2. Testing GET /api/user/:id...');
    const getUserResponse = await axios.get(`${BASE_URL}/api/user/${userId}`);
    console.log('✓ Profile retrieved:', getUserResponse.data);
    console.log('');

    // Test 3: POST /api/usage - Log usage
    console.log('3. Testing POST /api/usage...');
    const usageData = {
      user_id: userId,
      action: 'view_dashboard',
      metadata: { screen: 'dashboard', timestamp: Date.now() }
    };
    const usageResponse = await axios.post(`${BASE_URL}/api/usage`, usageData);
    console.log('✓ Usage logged:', usageResponse.data);
    console.log('');

    // Test 4: POST /api/recommend - Get recommendations
    console.log('4. Testing POST /api/recommend...');
    const recommendResponse = await axios.post(`${BASE_URL}/api/recommend`, profileData);
    console.log('✓ Recommendations received:', recommendResponse.data);
    console.log('');

    // Test 5: Validation - Missing fields
    console.log('5. Testing validation (missing fields)...');
    try {
      await axios.post(`${BASE_URL}/api/profile`, { income: 50000 });
    } catch (error) {
      if (error.response && error.response.status === 400) {
        console.log('✓ Validation error caught:', error.response.data.message);
      } else {
        throw error;
      }
    }
    console.log('');

    // Test 6: GET non-existent user
    console.log('6. Testing GET /api/user/:id with non-existent ID...');
    try {
      await axios.get(`${BASE_URL}/api/user/99999`);
    } catch (error) {
      if (error.response && error.response.status === 404) {
        console.log('✓ 404 error caught:', error.response.data.message);
      } else {
        throw error;
      }
    }
    console.log('');

    console.log('All tests passed! ✓');
  } catch (error) {
    console.error('Test failed:', error.message);
    if (error.response) {
      console.error('Response:', error.response.data);
    }
    process.exit(1);
  }
}

testEndpoints();
