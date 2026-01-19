import { Github, Linkedin, Twitter, Mail } from "lucide-react";

export function SocialLinks({ className = "", vertical = false }: { className?: string, vertical?: boolean }) {
  const links = [
    { icon: Github, href: "https://github.com/Rupesh-110805", label: "GitHub" },
    { icon: Linkedin, href: "https://linkedin.com/in/rupesh-nidadavolu", label: "LinkedIn" },
    { icon: Twitter, href: "https://twitter.com", label: "Twitter" },
    { icon: Mail, href: "mailto:rupeshnidadavolu110805@gmail.com", label: "Email" },
  ];

  return (
    <div className={`flex ${vertical ? 'flex-col gap-6' : 'gap-6'} ${className}`}>
      {links.map((link) => (
        <a
          key={link.label}
          href={link.href}
          target="_blank"
          rel="noreferrer"
          className="text-muted-foreground hover:text-primary hover:-translate-y-1 transition-all duration-200"
          aria-label={link.label}
        >
          <link.icon className="w-5 h-5" />
        </a>
      ))}
    </div>
  );
}
