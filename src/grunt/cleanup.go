package main

import (
	"bytes"
	"fmt"
	log "github.com/Sirupsen/logrus"
	"net/smtp"
	"strings"
	"text/template"
)

func Email(job *Job) {
	log.Printf("Mailing status for %v", job.UUID)
	if config.Mail.Server == "" {
		return
	}
	var auth smtp.Auth = nil
	if config.Mail.Username != "" && config.Mail.Password != "" {
		auth = smtp.PlainAuth("", config.Mail.Username, config.Mail.Password, config.Mail.Server)
	}

	var templateData = map[string]interface{}{
		"job":     job,
		"service": config.ServiceMap[job.Endpoint],
		"to":      strings.Trim(fmt.Sprint(job.Address), "[]"),
		"config":  config,
	}
	contents, _ := Asset("template/email.txt")
	t, _ := template.New("email").Parse(string(contents))
	var buffer bytes.Buffer
	err := t.Execute(&buffer, templateData)
	if err != nil {
		log.Printf("Failed to construct email: %v", err.Error())
		return
	}
	server := fmt.Sprintf("%s:%d", config.Mail.Server, config.Mail.Port)
	log.Printf("Sending to: %v", templateData["job"])
	log.Printf("With auth: %+v", auth)
	log.Printf("Body: \n%v", buffer.String())
	err = smtp.SendMail(server, auth, config.Mail.From, job.Address, buffer.Bytes())
	if err != nil {
		log.Errorf("Error sending mail: %v", err.Error())
	} else {
		log.Printf("Mail sent")
	}
}

func Cleanup(job *Job) {
	log.Printf("Cleaning up %v", job.UUID)
}
