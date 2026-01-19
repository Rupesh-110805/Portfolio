"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Menu, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { Link as ScrollLink } from "react-scroll";

const NAV_ITEMS = [
  { name: "About", to: "about" },
  { name: "Experience", to: "skills" },
  { name: "Projects", to: "projects" },
  { name: "Contact", to: "contact" },
];

export function Navigation() {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header 
      className={`fixed top-0 w-full z-50 transition-all duration-300 ${
        scrolled ? "bg-background/80 backdrop-blur-md shadow-sm border-b border-border/50 h-16" : "bg-transparent h-20"
      }`}
    >
      <div className="container mx-auto px-6 h-full flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="relative z-50">
          <div className="text-primary font-mono font-bold text-xl tracking-tighter cursor-pointer border-2 border-primary w-10 h-10 flex items-center justify-center rounded hover:bg-primary/10 transition-colors">
            DEV
          </div>
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-8">
          {NAV_ITEMS.map((item, i) => (
            <ScrollLink
              key={item.name}
              to={item.to}
              smooth={true}
              duration={500}
              className="text-sm font-mono text-muted-foreground hover:text-primary cursor-pointer transition-colors"
            >
              <span className="text-primary mr-1">0{i + 1}.</span>
              {item.name}
            </ScrollLink>
          ))}
          <a 
            href="/resume.pdf" 
            target="_blank"
            className="px-4 py-2 border border-primary text-primary font-mono text-sm rounded hover:bg-primary/10 transition-colors ml-4"
          >
            Resume
          </a>
        </nav>

        {/* Mobile Toggle */}
        <button 
          className="md:hidden z-50 text-foreground"
          onClick={() => setIsOpen(!isOpen)}
        >
          {isOpen ? <X /> : <Menu />}
        </button>

        {/* Mobile Menu */}
        <AnimatePresence>
          {isOpen && (
            <motion.div
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ type: "tween", duration: 0.3 }}
              className="fixed inset-y-0 right-0 w-3/4 bg-card border-l border-border shadow-2xl z-40 flex flex-col justify-center items-center md:hidden"
            >
              <nav className="flex flex-col gap-8 text-center">
                {NAV_ITEMS.map((item, i) => (
                  <ScrollLink
                    key={item.name}
                    to={item.to}
                    smooth={true}
                    duration={500}
                    onClick={() => setIsOpen(false)}
                    className="text-lg font-mono text-muted-foreground hover:text-primary cursor-pointer transition-colors"
                  >
                    <div className="text-primary text-sm mb-1">0{i + 1}.</div>
                    {item.name}
                  </ScrollLink>
                ))}
                <a 
                  href="/resume.pdf" 
                  target="_blank"
                  className="px-8 py-3 border border-primary text-primary font-mono text-sm rounded hover:bg-primary/10 transition-colors mt-4"
                >
                  Resume
                </a>
              </nav>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </header>
  );
}
