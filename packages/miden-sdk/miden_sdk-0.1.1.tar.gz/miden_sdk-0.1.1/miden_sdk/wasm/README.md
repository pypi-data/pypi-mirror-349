# WASM Module Directory

This directory should contain the WebAssembly (WASM) module for the Miden SDK.

## Required File

- `miden_sdk.wasm`: The WASM module from @demox-labs/miden-sdk

## How to Get the WASM Module

1. Install the @demox-labs/miden-sdk NPM package:
   ```bash
   npm install @demox-labs/miden-sdk
   ```

2. Copy the WASM module from the installed package:
   ```bash
   cp node_modules/@demox-labs/miden-sdk/dist/miden_sdk.wasm /path/to/miden-py/miden_sdk/wasm/
   ```

## Note

If the WASM module is not present, the SDK will still function, but WASM-dependent features like wallet creation through the WASM module will be unavailable. A warning will be logged when the module is not found. 