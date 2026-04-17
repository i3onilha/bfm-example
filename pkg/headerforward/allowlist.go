package headerforward

import "net/http"

// forwardAllowlist is the set of incoming request header names that may be
// propagated to backend HTTP calls. Keys must be in canonical form (see
// net/http.CanonicalHeaderKey).
var forwardAllowlist = map[string]struct{}{
	"Authorization":    {},
	"X-Correlation-Id": {},
	"X-Request-Id":     {},
	"X-Tenant-Id":      {},
	"Traceparent":      {},
	"Tracestate":       {},
}

// FilterHeaders returns a new Header containing only allowlisted entries from
// src. If nothing passes the filter, it returns nil.
func FilterHeaders(src http.Header) http.Header {
	if len(src) == 0 {
		return nil
	}
	out := make(http.Header)
	for key, values := range src {
		canonical := http.CanonicalHeaderKey(key)
		if _, ok := forwardAllowlist[canonical]; !ok {
			continue
		}
		for _, v := range values {
			out.Add(canonical, v)
		}
	}
	if len(out) == 0 {
		return nil
	}
	return out
}
