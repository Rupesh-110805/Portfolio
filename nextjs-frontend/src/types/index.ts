// Types matching FastAPI schemas

export interface Project {
  id: number;
  title: string;
  description: string;
  tech_stack: string[];
  link?: string | null;
  github_link?: string | null;
  image_url: string;
}

export interface ProjectCreate {
  title: string;
  description: string;
  tech_stack: string[];
  link?: string | null;
  github_link?: string | null;
  image_url: string;
}

export interface Skill {
  id: number;
  name: string;
  category: string;
}

export interface Message {
  id: number;
  name: string;
  email: string;
  message: string;
}

export interface MessageCreate {
  name: string;
  email: string;
  message: string;
}

// Alias for form compatibility (matching original schema naming)
export type InsertMessage = MessageCreate;
export type InsertProject = ProjectCreate;
