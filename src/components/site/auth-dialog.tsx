"use client";

import { useState } from "react";
import { KeyRound, LogIn, UserRound } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { loginRequest, registerRequest } from "@/lib/client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

interface AuthDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  /** 登录/注册成功回调 */
  onSuccess: (name: string) => void;
}

export function AuthDialog({ open, onOpenChange, onSuccess }: AuthDialogProps) {
  const { toast } = useToast();
  const [tab, setTab] = useState<"login" | "register">("login");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const reset = () => {
    setName("");
    setPassword("");
    setConfirm("");
    setError("");
    setBusy(false);
  };

  const handleClose = (v: boolean) => {
    if (!v) {
      reset();
      setTab("login");
    }
    onOpenChange(v);
  };

  const submit = async () => {
    setError("");
    if (!name.trim()) return setError("请输入用户名");
    if (!password) return setError("请输入密码");

    setBusy(true);
    try {
      if (tab === "register") {
        if (password.length < 6) {
          setBusy(false);
          return setError("密码至少 6 位");
        }
        if (password !== confirm) {
          setBusy(false);
          return setError("两次输入的密码不一致");
        }
        const res = await registerRequest(name.trim(), password);
        if (!res.ok) {
          setBusy(false);
          return setError(res.error || "注册失败");
        }
        toast({ title: `欢迎加入，${res.user?.name ?? name}！`, description: "做题记录已保存到你的账号" });
        handleClose(false);
        onSuccess(res.user?.name ?? name.trim());
      } else {
        const res = await loginRequest(name.trim(), password);
        if (!res.ok) {
          setBusy(false);
          return setError(res.error || "登录失败");
        }
        toast({ title: `欢迎回来，${res.user?.name ?? name}`, description: "云端做题记录已同步" });
        handleClose(false);
        onSuccess(res.user?.name ?? name.trim());
      }
    } finally {
      setBusy(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-primary font-mono text-xs font-bold text-primary-foreground">
              408
            </span>
            <span>
              账号登录<span className="ml-1 font-mono text-xs text-muted-foreground">auth()</span>
            </span>
          </DialogTitle>
          <DialogDescription>
            注册账号后，做题记录、收藏与模考成绩将持久保存，换设备登录也不丢。
          </DialogDescription>
        </DialogHeader>

        <Tabs value={tab} onValueChange={(v) => { setTab(v as "login" | "register"); setError(""); }}>
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="login" className="gap-1.5">
              <LogIn className="h-3.5 w-3.5" /> 登录
            </TabsTrigger>
            <TabsTrigger value="register" className="gap-1.5">
              <UserRound className="h-3.5 w-3.5" /> 注册
            </TabsTrigger>
          </TabsList>

          <TabsContent value="login" className="mt-4 space-y-4">
            <div className="space-y-2">
              <Label htmlFor="login-name">用户名</Label>
              <Input
                id="login-name"
                placeholder="用户名 / username"
                value={name}
                onChange={(e) => setName(e.target.value)}
                maxLength={20}
                autoComplete="username"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="login-password">密码</Label>
              <Input
                id="login-password"
                type="password"
                placeholder="••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
                onKeyDown={(e) => e.key === "Enter" && submit()}
              />
            </div>
          </TabsContent>

          <TabsContent value="register" className="mt-4 space-y-4">
            <div className="space-y-2">
              <Label htmlFor="reg-name">用户名</Label>
              <Input
                id="reg-name"
                placeholder="2-20 位，字母 / 数字 / 中文"
                value={name}
                onChange={(e) => setName(e.target.value)}
                maxLength={20}
                autoComplete="username"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="reg-password">密码</Label>
              <Input
                id="reg-password"
                type="password"
                placeholder="至少 6 位"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="new-password"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="reg-confirm">确认密码</Label>
              <Input
                id="reg-confirm"
                type="password"
                placeholder="再输入一次密码"
                value={confirm}
                onChange={(e) => setConfirm(e.target.value)}
                autoComplete="new-password"
                onKeyDown={(e) => e.key === "Enter" && submit()}
              />
            </div>
          </TabsContent>
        </Tabs>

        {error && (
          <p className="rounded-md bg-destructive/10 px-3 py-2 text-sm text-destructive" role="alert">
            {error}
          </p>
        )}

        <Button onClick={submit} disabled={busy} className="w-full gap-1.5">
          <KeyRound className="h-4 w-4" />
          {busy ? "请稍候…" : tab === "login" ? "登录" : "注册并登录"}
        </Button>

        <p className="text-center text-xs text-muted-foreground">
          未登录也可刷题（访客模式）；登录时当前记录会自动并入账号
        </p>
      </DialogContent>
    </Dialog>
  );
}
