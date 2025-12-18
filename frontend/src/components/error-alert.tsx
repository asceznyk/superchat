import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert"
import { AlertTriangle, X } from "lucide-react"
import { Button } from "@/components/ui/button"

type ErrorAlertProps = {
  message?: string
  onClose?: () => void
}

export function ErrorAlert({ message, onClose }: ErrorAlertProps) {
  return (
    <Alert variant="destructive" className="relative mb-4 mx-4 pr-10">
      <AlertTriangle className="h-4 w-4" />
      <div>
        <AlertTitle>Something went wrong</AlertTitle>
        <AlertDescription>
          {message ?? "Please try again in a moment."}
        </AlertDescription>
      </div>
      {onClose && (
        <Button
          variant="ghost"
          size="icon"
          onClick={onClose}
          className="absolute right-2 top-2 h-6 w-6"
        >
          <X className="h-4 w-4" />
        </Button>
      )}
    </Alert>
  )
}


