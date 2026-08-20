// Follow this setup guide to integrate the Deno language server with your editor:
// https://deno.land/manual/getting_started/setup_your_environment
// This enables autocomplete, go to definition, etc.

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

serve(async (req) => {
  try {
    const { filename, size } = await req.json()
    
    // Example validation logic
    if (!filename) {
      return new Response(
        JSON.stringify({ error: 'Filename is required' }),
        { headers: { "Content-Type": "application/json" }, status: 400 }
      )
    }

    console.log(`Processing uploaded file: ${filename}, Size: ${size} bytes`);
    
    // Custom server-side logic here!
    // Example: Check if file is too large (e.g., > 5MB)
    const MAX_SIZE = 5 * 1024 * 1024;
    let status = "Valid";
    
    if (size > MAX_SIZE) {
      status = "Warning: File size exceeds 5MB limit.";
      console.warn(status);
    }

    const data = {
      message: `Successfully processed metadata for ${filename}`,
      status: status,
      timestamp: new Date().toISOString()
    }

    return new Response(
      JSON.stringify(data),
      { headers: { "Content-Type": "application/json" } },
    )
  } catch (err) {
    return new Response(
      JSON.stringify({ error: err.message }),
      { headers: { "Content-Type": "application/json" }, status: 400 }
    )
  }
})
