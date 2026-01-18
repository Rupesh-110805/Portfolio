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
        title: "Algorithmic Trading Bot",
        description: "A Python-based trading bot that executes strategies based on technical indicators. Features backtesting capabilities and live trading integration with Alpaca API.",
        techStack: ["Python", "Pandas", "Docker", "AWS"],
        githubLink: "https://github.com/username/trading-bot",
        imageUrl: "https://images.unsplash.com/photo-1611974765270-ca12586343bb?auto=format&fit=crop&q=80&w=1000",
      },
      {
        title: "Compiler Design Project",
        description: "A custom compiler for a subset of the C language. Implemented lexical analysis, parsing, semantic analysis, and code generation.",
        techStack: ["C++", "LLVM", "Bison", "Flex"],
        githubLink: "https://github.com/username/mini-c-compiler",
        imageUrl: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&q=80&w=1000",
      },
      {
        title: "Distributed File System",
        description: "A scalable distributed file system inspired by GFS. Handles replication, fault tolerance, and consistency across multiple nodes.",
        techStack: ["Go", "gRPC", "Protobuf"],
        githubLink: "https://github.com/username/distributed-fs",
        imageUrl: "https://images.unsplash.com/photo-1558494949-ef2bb6db8744?auto=format&fit=crop&q=80&w=1000",
      },
      {
        title: "Neural Network Visualization",
        description: "Interactive web application to visualize how neural networks learn. Users can adjust hyperparameters and see real-time training progress.",
        techStack: ["TypeScript", "React", "D3.js", "TensorFlow.js"],
        link: "https://nn-viz.demo.com",
        githubLink: "https://github.com/username/nn-viz",
        imageUrl: "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&q=80&w=1000",
      }
    ]);
  }

  const existingSkills = await storage.getSkills();
  if (existingSkills.length === 0) {
    await db.insert(skills).values([
      // Languages
      { name: "TypeScript", category: "Languages" },
      { name: "Python", category: "Languages" },
      { name: "C++", category: "Languages" },
      { name: "Go", category: "Languages" },
      { name: "SQL", category: "Languages" },
      { name: "Rust", category: "Languages" },
      
      // Frameworks
      { name: "React", category: "Frameworks" },
      { name: "Next.js", category: "Frameworks" },
      { name: "Node.js", category: "Frameworks" },
      { name: "Express", category: "Frameworks" },
      { name: "Tailwind CSS", category: "Frameworks" },
      { name: "PyTorch", category: "Frameworks" },

      // Tools
      { name: "Git", category: "Tools" },
      { name: "Docker", category: "Tools" },
      { name: "Kubernetes", category: "Tools" },
      { name: "AWS", category: "Tools" },
      { name: "Linux", category: "Tools" },
      { name: "PostgreSQL", category: "Tools" },
    ]);
  }
}
