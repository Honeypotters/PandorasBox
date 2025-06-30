package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"
	"sync"
	"time"
)

type Response struct {
	Protocol      string            `json:"protocol"`
	StatusCode    int               `json:"status_code"`
	StatusMessage string            `json:"status_message"`
	Headers       map[string]string `json:"headers"`
}

type LLMResponse struct {
	Response string `json:"response"`
}

type ResponseWrapper struct {
	Response Response `json:"response"`
}

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
	// Time response
	start := time.Now()

	// Craft http request line
	var request strings.Builder
	request.WriteString(requestLineJson(req))

	for name, headers := range req.Header {
		if checkValidHeader(name) {
			for _, h := range headers {
				// May result in unnecessary final ','
				request.WriteString(fmt.Sprintf(",\n\"%v\": \"%v\"", name, h))
			}
		}
	}

	// Close remaining brackets of request
	request.WriteString("\n}\n}\n")
	response := postToLlm(request.String())

	// Update statistics
	AddRequest(request.String())
	LocateRequest(strings.SplitN(req.RemoteAddr, ":", 2)[0])
	AddResponse(response)

	var llmResponse LLMResponse
	err := json.Unmarshal([]byte(response), &llmResponse)
	if err != nil {
		log.Fatalf("Failed to unmarshal outer JSON: %v", err)
	}

	var responseWrapper ResponseWrapper
	err = json.Unmarshal([]byte(llmResponse.Response), &responseWrapper)
	if err != nil {
		log.Fatalf("Failed to unmarshal inner JSON string: %v", err)
	}

	for key, value := range responseWrapper.Response.Headers {
		if strings.ToLower(key) == "content-length" {
			continue
		}
		if key == "date" {
			headerTime, err := time.Parse(time.RFC3339, value)
			if err != nil {
				continue
			}
			w.Header().Set("Date", headerTime.UTC().Format(time.RFC3339))
		} else {
			w.Header().Set(key, value)
		}

	}

	w.WriteHeader(responseWrapper.Response.StatusCode)
	w.Write([]byte(responseWrapper.Response.StatusMessage))

	// Record and log time taken
	diff := time.Since(start)
	fmt.Printf("%v\n", diff.Seconds())
	AddTimeTaken(diff.Seconds())
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

	// Use a WaitGroup to ensure stats services are initialized before we proceed.
	var wg sync.WaitGroup
	wg.Add(1)

	// Start the stats server, passing the WaitGroup.
	go startStats(&wg)

	// Wait here until the stats service signals it has finished initializing.
	log.Println("Main: Waiting for stats service to initialize...")
	wg.Wait()
	log.Println("Main: Stats service initialized. Starting HTTP server.")

	// Now that stats are initialized, we can safely defer the DB closure.
	if geoDb != nil {
		defer geoDb.Close()
	}

	startHttpServer()
}

// Convert to json, send to api with request, receive the request, convert json to http request and return
