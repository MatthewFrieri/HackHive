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

// Generic POST helper
export async function postRequest<T, B = unknown>(
  endpoint: string,
  body: B,
): Promise<T> {
  try {
    const response = await api.post<T>(endpoint, body);
    return response.data;
  } catch (error: any) {
    console.error(`Error posting to ${endpoint}:`, error.message);
    throw error;
  }
}

export async function getData(): Promise<string[]> {
  return getRequest("/data");
}

type StartGamePayload = {
  players: string[];
  smallBlind: number;
  bigBlind: number;
  buyIn: number;
};

type StartGameResponse = {
  status: string;
};

export async function startGame(payload: StartGamePayload) {
  return postRequest<StartGameResponse, StartGamePayload>(
    "/start_game",
    payload,
  );
}
