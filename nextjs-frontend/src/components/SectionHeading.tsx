"use client";

import { motion } from "framer-motion";

interface SectionHeadingProps {
  number: string;
  title: string;
  className?: string;
}

export function SectionHeading({ number, title, className = "" }: SectionHeadingProps) {
  return (
    <motion.div 
      initial={{ opacity: 0, x: -20 }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
      className={`flex items-center gap-4 mb-8 md:mb-12 ${className}`}
    >
      <span className="text-primary font-mono text-lg md:text-xl font-medium">{number}.</span>
      <h2 className="text-2xl md:text-3xl font-bold tracking-tight text-foreground">{title}</h2>
      <div className="h-px bg-border flex-grow max-w-xs ml-4 hidden sm:block" />
    </motion.div>
  );
}
