package main

import (
	"fmt"
	"log"
	"net/http"
)

var validHeaders = map[string]bool{
	// placeholder
	"user-agent": true,
}

func headers(w http.ResponseWriter, req *http.Request) {
	// use a var to get only headers we want, then send them off
	for name, headers := range req.Header {
		for _, h := range headers {
			fmt.Fprintf(w, "%v: %v\n", name, h)
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
