// Package entity defines the core domain models.
package entity

// User represents a user in the system.
type User struct {
	ID    string `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
}
