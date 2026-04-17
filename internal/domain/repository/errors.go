package repository

import "errors"

// ErrUserNotFound is returned when a user ID does not resolve to a user.
// Implementations should wrap this value so callers can use errors.Is.
var ErrUserNotFound = errors.New("user not found")
