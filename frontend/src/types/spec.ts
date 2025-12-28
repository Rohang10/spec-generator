/* eslint-disable @typescript-eslint/no-explicit-any */
export interface Module {
  name: string;
  description?: string;
}

export interface UserStory {
  role: string;
  goal: string;
  benefit: string;
}

export interface APIEndpoint {
  method: string;
  path: string;
  auth_required: boolean;
  request_schema: Record<string, any>;
  response_schema: Record<string, any>;
  error_cases: string[];
}

export interface DBTable {
  table_name: string;
  columns: {
    name: string;
    type: string;
    constraints?: string;
  }[];
}

export interface SpecOutput {
  modules: Module[];
  features_by_module: Record<string, string[]>;
  user_stories: UserStory[];
  api_endpoints: APIEndpoint[];
  db_schema: DBTable[];
  open_questions: string[];
}

export type ApiError = {
  status: number;
  code: string;
  message: string;
};