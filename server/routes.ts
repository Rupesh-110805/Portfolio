import type { Express } from "express";
import type { Server } from "http";
import { storage } from "./storage";
import { api } from "@shared/routes";
import { z } from "zod";
import { projects, skills } from "@shared/schema";
import { db } from "./db";

export async function registerRoutes(
  httpServer: Server,
  app: Express
): Promise<Server> {
  // Projects
  app.get(api.projects.list.path, async (req, res) => {
    const projects = await storage.getProjects();
    res.json(projects);
  });

  app.post(api.projects.create.path, async (req, res) => {
    try {
      const input = api.projects.create.input.parse(req.body);
      const project = await storage.createProject(input);
      res.status(201).json(project);
    } catch (err) {
      if (err instanceof z.ZodError) {
        return res.status(400).json({ message: err.errors[0].message });
      }
      throw err;
    }
  });

  // Skills
  app.get(api.skills.list.path, async (req, res) => {
    const skills = await storage.getSkills();
    res.json(skills);
  });

  // Messages
  app.post(api.messages.create.path, async (req, res) => {
    try {
      const input = api.messages.create.input.parse(req.body);
      const message = await storage.createMessage(input);
      res.status(201).json(message);
    } catch (err) {
      if (err instanceof z.ZodError) {
        return res.status(400).json({ message: err.errors[0].message });
      }
      throw err;
    }
  });

  // Seed data if empty
  await seedDatabase();

  return httpServer;
}

async function seedDatabase() {
  const existingProjects = await storage.getProjects();
  if (existingProjects.length === 0) {
    await db.insert(projects).values([
      {
        title: "CSES-solutions",
        description: "A curated collection of solutions to problems on the CSES Problem Set. Solutions are written in modern C++, focused on competitive programming techniques like dynamic programming, graphs, and greedy algorithms.",
        techStack: ["C++", "Algorithms", "DSA"],
        githubLink: "https://github.com/Rupesh-110805/CSES-solutions",
        imageUrl: "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&q=80&w=1000",
      },
      {
        title: "DDOS_Project",
        description: "A Python project demonstrating a simulated DDOS attack tool with logging and basic protections. Explores network programming and multithreading concepts.",
        techStack: ["Python", "Networking", "Multithreading"],
        githubLink: "https://github.com/Rupesh-110805/DDOS_Project",
        imageUrl: "https://images.unsplash.com/photo-1558494949-ef2bb6db8744?auto=format&fit=crop&q=80&w=1000",
      },
      {
        title: "django-chat-app",
        description: "A real-time chat application built with Django and WebSockets. Users can exchange messages in chat rooms with session management and intuitive UI.",
        techStack: ["Django", "WebSockets", "PostgreSQL", "Redis"],
        githubLink: "https://github.com/Rupesh-110805/django-chat-app",
        imageUrl: "https://images.unsplash.com/photo-1611746435392-5021db4c2411?auto=format&fit=crop&q=80&w=1000",
      },
      {
        title: "Pneumonia-Detection-XAI",
        description: "A pneumonia detection model using CNN with explainable AI (XAI) visualizations on chest X-rays. Provides interpretability for medical imaging decisions.",
        techStack: ["Python", "PyTorch", "Deep Learning", "XAI"],
        githubLink: "https://github.com/Rupesh-110805/Pneumonia-Detection-XAI",
        imageUrl: "https://images.unsplash.com/photo-1530213786676-41ad9f7736f6?auto=format&fit=crop&q=80&w=1000",
      },
      {
        title: "Talent-flow",
        description: "A mini hiring platform built with TypeScript and modern frontend stack. Includes project-level features like search, filters, and intuitive UI components.",
        techStack: ["TypeScript", "React", "Frontend Design"],
        githubLink: "https://github.com/Rupesh-110805/Talent-flow",
        imageUrl: "https://images.unsplash.com/photo-1586281380349-632531db7ed4?auto=format&fit=crop&q=80&w=1000",
      }
    ]);
  }

  const existingSkills = await storage.getSkills();
  if (existingSkills.length === 0) {
    await db.insert(skills).values([
      // Programming Languages
      { name: "C++", category: "Programming Languages" },
      { name: "Python", category: "Programming Languages" },
      { name: "TypeScript", category: "Programming Languages" },
      
      // Frontend
      { name: "React", category: "Frontend" },
      { name: "TypeScript", category: "Frontend" },
      { name: "HTML", category: "Frontend" },
      { name: "CSS", category: "Frontend" },

      // Backend
      { name: "Django", category: "Backend" },

      // ML / AI
      { name: "Machine Learning", category: "ML / AI" },
      { name: "CNNs", category: "ML / AI" },
      { name: "Deep Learning", category: "ML / AI" },
      { name: "Explainable AI", category: "ML / AI" },

      // CS Core
      { name: "Data Structures", category: "CS Core" },
      { name: "Algorithms", category: "CS Core" },
      { name: "Competitive Programming", category: "CS Core" },

      // Systems / Networking
      { name: "Network Programming", category: "Systems / Networking" },
      { name: "Multithreading", category: "Systems / Networking" },

      // Tools / Others
      { name: "Git", category: "Tools / Others" },
      { name: "WebSockets", category: "Tools / Others" },
    ]);
  }
}
