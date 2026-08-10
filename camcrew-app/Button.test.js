import React, { useState } from 'react';
import { Button, Text, View } from 'react-native';
import { render, fireEvent, screen } from '@testing-library/react-native';

// A simple component to test
const HiddenMessage = () => {
  const [visible, setVisible] = useState(false);
  return (
    <View>
      <Button title="Show Message" onPress={() => setVisible(true)} />
      {visible && <Text>Hello from Camcrew!</Text>}
    </View>
  );
};

describe('User Interaction', () => {
  it('shows the message when the button is pressed', async () => {
    // 1. Render the component (await required for RNTL v14 + React 19)
    await render(<HiddenMessage />);

    // 2. Verify the message is NOT there initially using the screen object
    expect(screen.queryByText('Hello from Camcrew!')).toBeNull();

    // 3. Simulate a user tapping the button
    fireEvent.press(screen.getByText('Show Message'));

    // 4. Verify the message appears after the tap (await findByText waits for state re-render)
    expect(await screen.findByText('Hello from Camcrew!')).toBeTruthy();
  });
});