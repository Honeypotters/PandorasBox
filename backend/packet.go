package main

import (
	"fmt"
	"log"
	"time"

	"github.com/google/gopacket"
	"github.com/google/gopacket/layers"
	"github.com/google/gopacket/pcap"
)

var (
	snapshot_len int32         = 1024
	promiscuous  bool          = true
	timeout      time.Duration = 30 * time.Second
	handle       *pcap.Handle
)

func getDefaultInterface() (string, error) {
	devices, err := pcap.FindAllDevs()
	if err != nil {
		return "", err
	}

	for _, device := range devices {
		// Skip loopback and interfaces without addresses
		if len(device.Addresses) == 0 || device.Name == "lo" {
			continue
		}
		// Return first usable address until better method is implemented
		return device.Name, nil
	}
	return "", fmt.Errorf("no suitable network interface found")
}

func main() {
	device, err := getDefaultInterface()
	if err != nil {
		log.Fatalf("Could not find a suitable network interface: %v", err)
	}
	fmt.Printf("Using interface: %s\n", device)

	// Open device
	handle, err = pcap.OpenLive(device, snapshot_len, promiscuous, timeout)
	if err != nil {
		log.Fatal(err)
	}
	defer handle.Close()

	err = handle.SetBPFFilter("tcp and port 80 or port 443")
	if err != nil {
		log.Fatal(err)
	}

	// Use the handle as a packet source to process all packets
	packetSource := gopacket.NewPacketSource(handle, handle.LinkType())

	fmt.Println("Capturing packets...")
	for packet := range packetSource.Packets() {
		// Process packet
		if tcpLayer := packet.Layer(layers.LayerTypeTCP); tcpLayer != nil {
			tcp, _ := tcpLayer.(*layers.TCP)
			fmt.Printf("From port %d to %d\n", tcp.SrcPort, tcp.DstPort)
		}
	}
}
