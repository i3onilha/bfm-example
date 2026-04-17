// Package entity defines the core domain models.
package entity

// Order represents an order to be processed.
type Order struct {
	OrderID     string `json:"orderId"`
	UserID      string `json:"userId"`
	Priority    string `json:"priority"`
	Status      string `json:"status"`
	EstimatedAt string `json:"estimatedAt"`
}

// Priority constants.
const (
	PriorityHigh   = "high"
	PriorityNormal = "normal"
	PriorityLow    = "low"
)
