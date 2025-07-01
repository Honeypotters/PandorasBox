package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"net/netip"
	"os"
	"strings"
	"sync"
	"time"

	"github.com/gammazero/deque"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
	"github.com/oschwald/geoip2-golang/v2"
	"google.golang.org/genai"
)

type Uptime struct {
	UptimeMinutes int `json:"uptime_minutes"`
}

type AverageResponseTime struct {
	AverageResponseTime float64 `json:"average_response_time"`
}

type LastRequests struct {
	Requests []string `json:"last_10_requests"`
}

type LastResponses struct {
	Responses []string `json:"last_10_responses"`
}

type CategoryCounts struct {
	Counts map[string]int `json:"category_counts"`
}

type TagCounts struct {
	Counts map[string]int `json:"tag_counts"`
}

type Locations struct {
	Locations []Location `json:"locations"`
}

type Count struct {
	Count int `json:"count"`
}

type Location struct {
	Position [2]float64 `json:"position"`
	Name     string     `json:"name"`
}

type AIResponse struct {
	CategoryIndex int   `json:"primary_category"`
	TagIndices    []int `json:"tags"`
}

var startupTime = time.Now()

var responseTimes = new(deque.Deque[float64])

var requests = new(deque.Deque[string])
var requestCount = 0

var responses = new(deque.Deque[string])
var responseCount = 0

var categories = [5]string{"Reconnaissance & Scanning", "Exploitation Attempt", "Internet Noise", "Manual Investigation", "Uncategorized or Novel"}
var categorisedCounts = make(map[string]int)

var tags [15]string = [15]string{"Directory & File Probing", "Vulnerability Scanning", "Technology Fingerprinting", "SQL Injection (SQLi)", "Command & Code Injection (RCE)", "File Inclusion (LFI/RFI)", "Search Engine Crawler", "Security Research Scanner", "Service Heartbeat/Webhook", "Sequential Endpoint Testing", "Form Tampering", "Cookie & Header Manipulation", "Malformed or Corrupted Request", "Zero-Day Signature", "Protocol Mismatch"}
var tagCounts = make(map[string]int)

var googleAiAPIKey = ""
var geminiClient *genai.Client
var prompt = ""

var geoDb *geoip2.Reader
var locations = []Location{}

func getUptime(c *gin.Context) {
	uptime := Uptime{
		UptimeMinutes: int(time.Since(startupTime).Abs().Minutes()),
	}
	c.JSON(http.StatusOK, uptime)
}

func getRequestCount(c *gin.Context) {
	c.JSON(http.StatusOK, Count{Count: requestCount})
}

func getAverageResponseTime(c *gin.Context) {
	if responseTimes.Len() == 0 {
		c.JSON(http.StatusOK, AverageResponseTime{AverageResponseTime: 0})
		return
	}
	var total float64
	for i := 0; i < responseTimes.Len(); i++ {
		v := (*responseTimes).At(i)
		total += float64(v)
	}
	avgTime := AverageResponseTime{
		AverageResponseTime: total / float64(responseTimes.Len()),
	}
	c.JSON(http.StatusOK, avgTime)
}

func getLastTenRequests(c *gin.Context) {
	results := make([]string, 0, 10)
	for i := requests.Len() - 1; i >= 0 && len(results) < 10; i-- {
		results = append(results, requests.At(i))
	}
	lastReqs := LastRequests{
		Requests: results,
	}
	c.JSON(http.StatusOK, lastReqs)
}

func getLastTenResponses(c *gin.Context) {
	results := make([]string, 0, 10)
	for i := responses.Len() - 1; i >= 0 && len(results) < 10; i-- {
		results = append(results, responses.At(i))
	}
	lastResps := LastResponses{
		Responses: results,
	}
	c.JSON(http.StatusOK, lastResps)
}

func getCategorisedCounts(c *gin.Context) {
	catCounts := CategoryCounts{
		Counts: categorisedCounts,
	}
	c.JSON(http.StatusOK, catCounts)
}

func getTagCounts(c *gin.Context) {
	tagCountsResp := TagCounts{
		Counts: tagCounts,
	}
	c.JSON(http.StatusOK, tagCountsResp)
}

func getLocations(c *gin.Context) {
	locsResp := Locations{
		Locations: locations,
	}

	c.JSON(http.StatusOK, locsResp)
}

func getLogfile(c *gin.Context) {
	content, err := os.ReadFile("logs/log.txt")
	if err != nil {
		log.Printf("Could not read logfile: %v", err)
		c.String(http.StatusInternalServerError, "could not read logfile")
		return
	}

	c.String(http.StatusOK, string(content))
}

func AddRequest(request string) {
	if requests.Len() >= 10 {
		requests.PopFront()
	}

	requests.PushBack(request)
	requestCount++

	categoriseRequest(request)
}

func AddResponse(response string) {
	if responses.Len() >= 10 {
		responses.PopFront()
	}

	responses.PushBack(response)
	responseCount++
}

// Adds a time to queue of response times
func AddTimeTaken(time float64) {
	if responseTimes.Len() >= 10 {
		responseTimes.PopFront()
	}

	responseTimes.PushBack(time)
}

func initGemini() *genai.Client {
	ctx := context.Background()

	if googleAiAPIKey == "" {
		log.Fatal("GEMINI_API_KEY environment variable not set")
		os.Exit(1)
	}

	client, err := genai.NewClient(ctx, &genai.ClientConfig{
		APIKey:  googleAiAPIKey,
		Backend: genai.BackendGeminiAPI,
	})

	if err != nil {
		log.Fatalf("failed to create client: %v", err)
		os.Exit(1)
	}

	return client
}

func categoriseRequest(request string) {
	if requests.Len() == 0 {
		return
	}

	ctx := context.Background()

	if prompt == "" {
		log.Printf("GEMINI_PROMPT environment variable not set. Skipping categorization for: %s", request)
		return
	}

	fullPrompt := fmt.Sprintf(prompt, request)

	resp, err := geminiClient.Models.GenerateContent(ctx, "gemini-2.0-flash", genai.Text(fullPrompt), nil)
	if err != nil {
		log.Printf("Error generating content from Gemini: %v", err)
		return
	}

	aiResponseText := resp.Text()

	if aiResponseText == "" {
		log.Printf("No text content generated from Gemini for request: %s", request)
		log.Printf("Raw Gemini response: %+v", resp)
		return
	}

	cleanedResponseText := strings.TrimPrefix(aiResponseText, "```json")
	cleanedResponseText = strings.TrimSuffix(cleanedResponseText, "```")
	cleanedResponseText = strings.TrimSpace(cleanedResponseText)

	var aiResponse AIResponse
	err = json.Unmarshal([]byte(cleanedResponseText), &aiResponse)
	if err != nil {
		log.Printf("Error unmarshalling JSON from AI: %v. Response text was: '%s'", err, cleanedResponseText)
		categorisedCounts["Uncategorized or Novel"]++
		return
	}

	log.Printf("AI response for request '%s': %+v", request, aiResponse)

	if aiResponse.CategoryIndex >= 0 && aiResponse.CategoryIndex < len(categories) {
		category := categories[aiResponse.CategoryIndex]
		categorisedCounts[category]++
	} else {
		log.Printf("Invalid category index '%d' returned by AI. Defaulting to 'Uncategorized or Novel'.", aiResponse.CategoryIndex)
		categorisedCounts["Uncategorized or Novel"]++
	}

	for _, tagIndex := range aiResponse.TagIndices {
		if tagIndex >= 0 && tagIndex < len(tags) {
			tag := tags[tagIndex]
			tagCounts[tag]++
		} else {
			log.Printf("Invalid tag index '%d' returned by AI. Skipping.", tagIndex)
		}
	}
}

func initGeoIP() *geoip2.Reader {
	db, err := geoip2.Open("GeoLite2-City.mmdb")
	if err != nil {
		log.Fatalf("CRITICAL: Error opening GeoIP database: %v", err)
	}
	return db
}

func LocateRequest(requestIP string) {
	if geoDb == nil {
		log.Println("GeoIP database not initialized. Skipping location lookup.")
		return
	}

	ip, err := netip.ParseAddr(requestIP)
	if err != nil {
		log.Printf(err.Error())
		return
	}
	record, err := geoDb.City(ip)
	if err != nil {
		log.Printf("Error looking up IP %s: %v", requestIP, err)
		return
	}
	if !record.HasData() {
		log.Printf("No location data found for IP %s", requestIP)
		return
	}

	location := record.Location
	lat := *location.Latitude
	lon := *location.Longitude

	city := record.City.Names.English
	country := record.Country.Names.English

	result := Location{
		Position: [2]float64{lat, lon},
		Name:     fmt.Sprintf("%s, %s", city, country),
	}

	locations = append(locations, result)
}

func startStats(wg *sync.WaitGroup) {
	fmt.Println("Stats Server starting...")

	// Load environment variables from .env file
	err := godotenv.Load()
	if err != nil {
		log.Println("Warning: Error loading .env file, continuing with environment variables.")
	}
	googleAiAPIKey = os.Getenv("GEMINI_API_KEY")
	prompt = os.Getenv("GEMINI_PROMPT")

	// Initialize the Google Gemini AI client
	geminiClient = initGemini()

	// Initialize GeoIP database
	geoDb = initGeoIP()

	// initialize count maps
	for _, category := range categories {
		categorisedCounts[category] = 0
	}
	for _, tag := range tags {
		tagCounts[tag] = 0
	}

	// Initialization is complete
	log.Println("Stats service initialization finished.")
	// Signal to the main function that it can proceed.
	wg.Done()

	// Set up the Gin router
	router := gin.Default()
	router.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"*"},
		AllowMethods:     []string{"GET"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Accept", "Authorization"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}))

	router.GET("/uptime", getUptime)
	router.GET("/average-response-time", getAverageResponseTime)
	router.GET("/last-ten-requests", getLastTenRequests)
	router.GET("/last-ten-responses", getLastTenResponses)
	router.GET("/categorised-counts", getCategorisedCounts)
	router.GET("/tag-counts", getTagCounts)
	router.GET("/locations", getLocations)
	router.GET("/request-count", getRequestCount)
	router.GET("/logfile", getLogfile)

	// Start the server
	router.Run(":8080")
}
