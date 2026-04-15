export interface UserMessage {
    id: string;
    senderId: string;
    text: string;
    timestamp: number;
}

export interface AgentResponse {
    reply: string;
    contextDetected?: string;
    intent?: 'query' | 'buy' | 'unknown';
}
