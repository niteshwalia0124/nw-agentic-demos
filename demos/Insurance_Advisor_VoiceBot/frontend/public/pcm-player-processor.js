/**
 * An audio worklet processor that stores the PCM audio data sent from the main thread
 * to a buffer and plays it.
 */
class PCMPlayerProcessor extends AudioWorkletProcessor {
  constructor() {
    super();

    // Init buffer
    this.bufferSize = 24000 * 180;  // 24kHz x 180 seconds
    this.buffer = new Float32Array(this.bufferSize);
    this.writeIndex = 0;
    this.readIndex = 0;
    
    // Jitter buffer settings
    this.minBufferToPlay = 24000 * 0.5; // 500ms of audio at 24kHz (increased to reduce crackiness)
    this.isBuffering = true;

    // Handle incoming messages from main thread
    this.port.onmessage = (event) => {
      // Reset the buffer when 'endOfAudio' message received
      if (event.data.command === 'endOfAudio') {
        this.readIndex = this.writeIndex; // Clear the buffer
        this.isBuffering = true;
        console.log("endOfAudio received, clearing the buffer.");
        return;
      }

      // Decode the base64 data to int16 array.
      const int16Samples = new Int16Array(event.data);

      // Add the audio data to the buffer
      this._enqueue(int16Samples);
    };
  }

  // Get current buffer length
  _getBufferLength() {
    return (this.writeIndex - this.readIndex + this.bufferSize) % this.bufferSize;
  }

  // Push incoming Int16 data into our ring buffer.
  _enqueue(int16Samples) {
    for (let i = 0; i < int16Samples.length; i++) {
      // Convert 16-bit integer to float in [-1, 1]
      const floatVal = int16Samples[i] / 32768;

      // Store in ring buffer for left channel only (mono)
      this.buffer[this.writeIndex] = floatVal;
      this.writeIndex = (this.writeIndex + 1) % this.bufferSize;

      // Overflow handling (overwrite oldest samples)
      if (this.writeIndex === this.readIndex) {
        this.readIndex = (this.readIndex + 1) % this.bufferSize;
      }
    }
    
    // Stop buffering if we have reached the threshold
    if (this.isBuffering && this._getBufferLength() >= this.minBufferToPlay) {
      this.isBuffering = false;
    }
  }

  // The system calls `process()` ~128 samples at a time (depending on the browser).
  // We fill the output buffers from our ring buffer.
  process(inputs, outputs, parameters) {

    // Write a frame to the output
    const output = outputs[0];
    const framesPerBlock = output[0].length;
    for (let frame = 0; frame < framesPerBlock; frame++) {

      // Play only if not buffering and we have data
      if (!this.isBuffering && this.readIndex !== this.writeIndex) {
        output[0][frame] = this.buffer[this.readIndex]; // left channel
        if (output.length > 1) {
          output[1][frame] = this.buffer[this.readIndex]; // right channel
        }
        this.readIndex = (this.readIndex + 1) % this.bufferSize;
        
        // If we run dry, go back to buffering mode
        if (this.readIndex === this.writeIndex) {
          this.isBuffering = true;
        }
      } else {
        // Output silence if buffering or truly empty
        output[0][frame] = 0;
        if (output.length > 1) {
          output[1][frame] = 0;
        }
      }
    }

    // Returning true tells the system to keep the processor alive
    return true;
  }
}

registerProcessor('pcm-player-processor', PCMPlayerProcessor);
