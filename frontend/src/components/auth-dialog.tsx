import { useState } from "react"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Separator } from "@/components/ui/separator"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

function GoogleIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      viewBox="0 0 48 48"
      width="20"
      height="20"
      {...props}
    >
      <path fill="#EA4335" d="M24 9.5c3.54 0 6.73 1.22 9.22 3.6l6.9-6.9C35.9 2.4 30.47 0 24 0 14.6 0 6.4 5.38 2.54 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
      <path fill="#4285F4" d="M46.5 24c0-1.64-.15-3.22-.43-4.75H24v9h12.7c-.55 2.98-2.22 5.5-4.7 7.2l7.27 5.64C43.7 36.9 46.5 30.95 46.5 24z"/>
      <path fill="#FBBC05" d="M10.52 28.59a14.47 14.47 0 0 1 0-9.18l-7.98-6.19a24 24 0 0 0 0 21.56l7.98-6.19z"/>
      <path fill="#34A853" d="M24 48c6.47 0 11.9-2.13 15.87-5.81l-7.27-5.64c-2.02 1.36-4.6 2.16-8.6 2.16-6.26 0-11.57-4.22-13.48-9.91l-7.98 6.19C6.4 42.62 14.6 48 24 48z"/>
    </svg>
  )
}

interface AuthDialogProps {
  text: string;
}

export function AuthDialog({ text }: AuthDialogProps) {
  const [open, setOpen] = useState(false)
  const baseBtn = "rounded-full cursor-pointer"
  const baseInput = "rounded-full"
  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button className={baseBtn} variant="outline">{text}</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[420px]">
        <DialogHeader>
          <DialogTitle>{text}</DialogTitle>
        </DialogHeader>
        <Button className={baseBtn} variant="outline">
          <GoogleIcon />
          Continue with Google
        </Button>
        <Separator className="my-4" />
        <Input className={baseInput} placeholder="Continue with email" />
        <Button className={baseBtn}>Continue</Button>
      </DialogContent>
    </Dialog>
  )
}

