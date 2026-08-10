import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react-native';
// Adjust this path if your test folder is located somewhere else
import { Button } from '../src/components/ui/Button'; 

describe('Button Component', () => {
  // Test 1: Does it render correctly?
  it('renders the correct title', async () => {
    await render(<Button title="Submit" onPress={() => {}} />);
    expect(screen.getByText('Submit')).toBeTruthy();
  });

  // Test 2: Does the onPress function actually fire?
  it('fires the onPress function when tapped', async () => {
    // Create a mock function (a "spy") to track interactions
    const mockPress = jest.fn();
    await render(<Button title="Click Me" onPress={mockPress} />);

    // Simulate the user tapping the button
    fireEvent.press(screen.getByText('Click Me'));

    // Verify the mock function was triggered exactly one time
    expect(mockPress).toHaveBeenCalledTimes(1);
  });

  // Test 3: Does it prevent interactions when disabled?
  it('does not fire onPress when disabled is true', async () => {
    const mockPress = jest.fn();
    await render(<Button title="Disabled" onPress={mockPress} disabled={true} />);

    // Attempt to tap the disabled button
    fireEvent.press(screen.getByText('Disabled'));

    // Verify the mock function was NEVER triggered
    expect(mockPress).not.toHaveBeenCalled();
  });
});