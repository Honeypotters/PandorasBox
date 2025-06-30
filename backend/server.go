package main

import (
	"fmt"
	"log"
	"net/http"
	"strings"
)

var validHeaders = map[string]bool{
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

func requestLineJson(req *http.Request) string {
	var sb strings.Builder
	// Construct JSON formatting of request
	sb.WriteString("{\n\"prompt\": {\n")
	sb.WriteString(fmt.Sprintf("\"method\": \"%v\",\n", req.Method))
	sb.WriteString(fmt.Sprintf("\"url\": \"%v\",\n", req.URL))
	sb.WriteString(fmt.Sprintf("\"protocol\": \"%v\",\n", req.Proto))
	return sb.String()
}

func getResponseJson(w http.ResponseWriter, req *http.Request) {
	// Craft http request line
	var request strings.Builder
	request.WriteString(requestLineJson(req))

	for name, headers := range req.Header {
		if checkValidHeader(name) {
			for _, h := range headers {
				// May result in unnecessary final ','
				request.WriteString(fmt.Sprintf("\"%v\": \"%v\",\n", name, h))
			}
		}
	}
	// Close remaining brackets of request
	request.WriteString("}\n}\n")
	fmt.Fprint(w, request.String())
}

func startHttpServer() {
	log.Println("Starting HTTP Server on port 80")
	err := http.ListenAndServe(":80", nil)
	if err != nil {
		log.Fatalf("HTTP server failed: %v", err)
	}
}

func main() {
	http.HandleFunc("/", getResponseJson)

	startStats()
	startHttpServer()
}
