import { motion } from "framer-motion";
import { Github, ExternalLink, Folder } from "lucide-react";
import type { Project } from "@shared/schema";

interface ProjectCardProps {
  project: Project;
  index: number;
}

export function ProjectCard({ project, index }: ProjectCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.1, duration: 0.5 }}
      className="group relative bg-card rounded-lg overflow-hidden border border-border hover:border-primary/50 transition-colors duration-300 flex flex-col h-full"
    >
      {/* Image Overlay */}
      <div className="relative aspect-video overflow-hidden bg-muted">
        {project.imageUrl ? (
          <img 
            src={project.imageUrl} 
            alt={project.title} 
            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-muted-foreground">
            <Folder className="w-12 h-12 opacity-20" />
          </div>
        )}
        <div className="absolute inset-0 bg-primary/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      </div>

      <div className="p-6 flex flex-col flex-grow">
        <div className="flex justify-between items-start mb-4">
          <Folder className="w-8 h-8 text-primary" />
          <div className="flex gap-4">
            {project.githubLink && (
              <a 
                href={project.githubLink}
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted-foreground hover:text-primary transition-colors"
                title="View Source"
              >
                <Github className="w-5 h-5" />
              </a>
            )}
            {project.link && (
              <a 
                href={project.link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted-foreground hover:text-primary transition-colors"
                title="Live Demo"
              >
                <ExternalLink className="w-5 h-5" />
              </a>
            )}
          </div>
        </div>

        <h3 className="text-xl font-bold mb-2 group-hover:text-primary transition-colors font-mono">
          {project.title}
        </h3>
        
        <p className="text-muted-foreground mb-6 text-sm leading-relaxed flex-grow">
          {project.description}
        </p>

        <div className="flex flex-wrap gap-2 mt-auto">
          {project.techStack.map((tech) => (
            <span 
              key={tech} 
              className="text-xs font-mono text-primary/80"
            >
              {tech}
            </span>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
