import { object, string } from "zod";

export const signInSchema = object({
  email: string({ required_error: "Email is required" })
    .min(3, "Email is required")
    .email("Invalid email"),
  password: string({ required_error: "Password is required" })
    .min(3, "Password is required")
    .min(8, "Password must be at least 8 characters long")
    .max(32, "Password must be less than 32 characters long"),
});