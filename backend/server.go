package main

import (
	"bytes"
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
	sb.WriteString(fmt.Sprintf("\"protocol\": \"%v\"", req.Proto))
	return sb.String()
}

func postToLlm(request string) string {
	url := "http://127.0.0.1:5000/api"
	body := strings.NewReader(request)

	resp, err := http.Post(url, "application/json", body)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	buf := new(bytes.Buffer)
	_, err = buf.ReadFrom(resp.Body)
	if err != nil {
		log.Fatal(err)
	}
	return buf.String()
}

func getResponseJson(w http.ResponseWriter, req *http.Request) {
	// Craft http request line
	var request strings.Builder
	request.WriteString(requestLineJson(req))

	for name, headers := range req.Header {
		if checkValidHeader(name) {
			for _, h := range headers {
				// May result in unnecessary final ','
				//request.WriteString(fmt.Sprintf("\"%v\": \"%v\",\n", name, h))
				request.WriteString(fmt.Sprintf(",\n\"%v\": \"%v\"", name, h))
			}
		}
	}

	// Close remaining brackets of request
	request.WriteString("\n}\n}\n")
	fmt.Fprintf(w, "%s", request.String())
	AddRequest(request.String())
	LocateRequest(strings.SplitN(req.RemoteAddr, ":", 2)[0])

	response := postToLlm(request.String())
	AddResponse(response)
	fmt.Fprintf(w, "%s", response)
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

// Convert to json, send to api with request, receive the request, convert json to http request and return
