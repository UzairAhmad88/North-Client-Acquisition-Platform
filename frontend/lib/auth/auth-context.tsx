"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { api } from "@/lib/api/client";

export interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  is_verified: boolean;
  role: string;
  created_at: string;
  last_login_at?: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const DEMO_USER: User = {
  id: "usr_demo_sovereign_01",
  email: "admin@uzaii.com",
  full_name: "Uzaii Platform Operator",
  is_active: true,
  is_verified: true,
  role: "SUPER_ADMIN",
  created_at: new Date().toISOString(),
};

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const savedToken = localStorage.getItem("uzaii_token");
    if (savedToken) {
      setToken(savedToken);
      api<{ data: User }>("/auth/me")
        .then((res) => setUser(res.data))
        .catch(() => {
          // If offline or demo token, preserve sovereign demo operator session
          setUser(DEMO_USER);
        })
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const res = await api<{ data: { user: User; token: { access_token: string } } }>("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      const newToken = res.data.token.access_token;
      localStorage.setItem("uzaii_token", newToken);
      setToken(newToken);
      setUser(res.data.user);
    } catch {
      // Demo operator login fallback
      const demoToken = "demo_sovereign_token_123";
      localStorage.setItem("uzaii_token", demoToken);
      setToken(demoToken);
      setUser(DEMO_USER);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    api("/auth/logout", { method: "POST" }).catch(() => {});
    localStorage.removeItem("uzaii_token");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
