// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';

// Mock global functions or objects if needed
// Example: Mocking window.fetch
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({}),
  })
);

// Extend expect with custom matchers
// Example: Adding a matcher for accessibility checks using jest-axe
// Uncomment if using jest-axe for accessibility testing
// import 'jest-axe/extend-expect';

// Set up global variables or spies
beforeEach(() => {
  jest.clearAllMocks(); // Clears mocks before each test
});

// Handle unhandled promise rejections (helps debug async errors)
process.on('unhandledRejection', (reason) => {
  console.error('Unhandled Rejection:', reason);
});

// Mock a global console error or warn for specific messages to keep test logs clean
const originalError = console.error;
console.error = (...args) => {
  if (args[0].includes('some specific warning to ignore')) return;
  originalError(...args);
};

// Add custom utilities or global configurations for your tests
// Example: A utility function to render with a specific context provider
export const customRender = (ui, { providerProps, ...renderOptions } = {}) => {
  return render(ui, { wrapper: MyContextProvider, ...renderOptions });
};
