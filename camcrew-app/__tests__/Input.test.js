import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react-native';
import { Input } from '../src/components/ui/Input';

describe('Input Component', () => {
  it('calls onChangeText with the correct input when the user types', async () => {
    const mockOnChangeText = jest.fn();
    await render(
      <Input placeholder="Enter your name" onChangeText={mockOnChangeText} value="" />
    );
    const inputElement = screen.getByPlaceholderText('Enter your name');
    fireEvent.changeText(inputElement, 'Camcrew User');
    expect(mockOnChangeText).toHaveBeenCalledWith('Camcrew User');
  });

  it('displays the error message when the error prop is provided', async () => {
    await render(
      <Input placeholder="Email" error="Invalid email address" value="" onChangeText={() => {}} />
    );
    expect(screen.getByText('Invalid email address')).toBeTruthy();
  });
});