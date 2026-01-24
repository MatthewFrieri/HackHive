import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000", // change port if needed
  headers: {
    "Content-Type": "application/json",
  },
});

// Generic GET helper
export async function getRequest<T>(endpoint: string): Promise<T> {
  try {
    const response = await api.get<T>(endpoint);
    return response.data;
  } catch (error: any) {
    console.error(`Error fetching ${endpoint}:`, error.message);
    throw error;
  }
}

export async function getData(): Promise<string[]> {
  return getRequest("/data");
}
