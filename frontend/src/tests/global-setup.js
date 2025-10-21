// Global setup that runs before any imports
// This ensures localStorage is available before MSW initializes

// Mock localStorage for MSW and other components
const localStorageMock = {
  getItem: () => null,
  setItem: () => null,
  removeItem: () => null,
  clear: () => null,
  length: 0,
  key: () => null,
};

// Define localStorage on global and window objects
if (typeof global !== 'undefined') {
  Object.defineProperty(global, 'localStorage', {
    value: localStorageMock,
    writable: true,
  });
}

if (typeof window !== 'undefined') {
  Object.defineProperty(window, 'localStorage', {
    value: localStorageMock,
    writable: true,
  });
}
