import React, { useEffect, useState } from 'react';
import { Text, View } from 'react-native';
import { render, screen, waitFor } from '@testing-library/react-native';

// A sample component that fetches data
const UserProfile = () => {
  const [name, setName] = useState('Loading...');

  useEffect(() => {
    fetch('https://api.camcrew.com/user')
      .then(res => res.json())
      .then(data => setName(data.name))
      .catch(() => setName('Error fetching data'));
  }, []);

  return <View><Text>{name}</Text></View>;
};

describe('Network Requests', () => {
  // Clear any previous mocks before each test runs
  beforeEach(() => {
    global.fetch = jest.fn();
  });

  it('displays user data after a successful fetch', async () => {
    // 1. Force fetch to return a successful response with fake data
    global.fetch.mockResolvedValueOnce({
      json: jest.fn().mockResolvedValueOnce({ name: 'Alex Designer' }),
    });

    // 2. Render the component (await required for RNTL v14 + React 19)
    await render(<UserProfile />);

    // 3. Verify the loading state appears first (or check async resolution)
    await waitFor(() => {
      expect(screen.getByText('Alex Designer')).toBeTruthy();
    });
  });
it('displays an error message when the fetch fails', async () => {
    // 1. Force the fetch to fail
    global.fetch.mockRejectedValueOnce(new Error('Network error'));

    // 2. Render the component
    await render(<UserProfile />);

    // 3. Wait for the error state to appear ⚠️
    await waitFor(() => {
      expect(screen.getByText('Error fetching data')).toBeTruthy();
    });
  });
});