package headerforward

import (
	"net/http"
	"reflect"
	"testing"
)

func TestFilterHeaders(t *testing.T) {
	t.Parallel()

	src := http.Header{
		"Authorization":    []string{"Bearer x"},
		"X-Tenant-Id":      []string{"t1"},
		"Cookie":           []string{"session=secret"},
		"X-Evil-Forwarded": []string{"no"},
	}

	got := FilterHeaders(src)
	want := http.Header{
		"Authorization": []string{"Bearer x"},
		"X-Tenant-Id":   []string{"t1"},
	}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("FilterHeaders() = %#v, want %#v", got, want)
	}
}

func TestFilterHeaders_empty(t *testing.T) {
	t.Parallel()
	if got := FilterHeaders(nil); got != nil {
		t.Fatalf("FilterHeaders(nil) = %#v, want nil", got)
	}
	if got := FilterHeaders(http.Header{}); got != nil {
		t.Fatalf("FilterHeaders(empty) = %#v, want nil", got)
	}
}
