package main

import (
	"fmt"
	"log"
	"net/http"
	"strings"
)

var validHeaders = map[string]bool{
	// placeholder
	"host":            true,
	"user-agent":      true,
	"accept":          true,
	"accept-language": true,
	"accept-encoding": true,
	"x-csrf-token":    true,
	"referer":         true,
}

func checkValidHeader(header string) bool {
	return validHeaders[strings.ToLower(header)]
}

func headers(w http.ResponseWriter, req *http.Request) {
	// use a var to get only headers we want, then send them off
	for name, headers := range req.Header {
		if checkValidHeader(name) {
			for _, h := range headers {

				fmt.Fprintf(w, "%v: %v\n", name, h)

			}
		}
	}
}

func startHttpServer() {
	log.Println("Starting HTTP Server on port 80")
	err := http.ListenAndServe(":80", nil)
	if err != nil {
		log.Fatalf("HTTP server failed: %v", err)
	}
}

func main() {
	http.HandleFunc("/headers", headers)

	startHttpServer()
}
