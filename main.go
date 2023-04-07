package main

import (
	"fmt"
  "io"
	"log"
	"net/http"
  "regexp"
  "strconv"
  "os"
  "sync"

  "github.com/joho/godotenv"
)

func main(){
  data := make(chan string)
  done := make(chan bool)
  wg := sync.WaitGroup{}

  token := getEnvVar("GITHUB_TOKEN")
  url := getEnvVar("BASE_URL")
  pages := getPages(token,url)

  for i := 0; i < pages; i++ {
    wg.Add(1)
    go getRepos(data, &wg, i+1, token,url)
  }
  go consume(data, done)
  go func() {
      wg.Wait()
      close(data)
  }()
  d := <-done
  if d == true {
      fmt.Println("File written successfully")
  } else {
      fmt.Println("File writing failed")
  }
}

func getEnvVar(key string) string {
  err := godotenv.Load(".env")
  if err != nil {
    log.Fatalf("Error loading .env file")
  }

  return os.Getenv(key)
}

func consume(data chan string, done chan bool){
    f, err := os.Create("repos")
    if err != nil {
        fmt.Println(err)
        return
    }
    for d := range data {
        _, err = fmt.Fprintln(f, d)
        if err != nil {
            fmt.Println(err)
            f.Close()
            done <- false
            return
        }
    }
    err = f.Close()
    if err != nil {
        fmt.Println(err)
        done <- false
        return
    }
    done <- true
}


func setHeaders(req *http.Request, token string){
	req.Header.Set("Accept", "application/vnd.github+json")
	req.Header.Set("Authorization","Bearer "+token)
	req.Header.Set("X-GitHub-Api-Version","2022-11-28")
}

func getPages(token string,url string)(int) {
	client := &http.Client{}
  perPage := "?per_page=100"
	req, err := http.NewRequest("HEAD", url + perPage, nil)
	if err != nil {
		log.Fatal(err)
	}
  setHeaders(req,token)
	resp, err := client.Do(req)
	if err != nil {
		log.Fatal(err)
	}

	defer resp.Body.Close()
  if links,ok := resp.Header["Link"]; ok{
    pattern := regexp.MustCompile(`=(?P<Page>\d+)>; rel=\"last\"$`)
    matches := pattern.FindStringSubmatch(links[0])
    pageidx := pattern.SubexpIndex("Page")
    page, _ := strconv.Atoi(matches[pageidx])
    return page
  }
  return 1
}

func getRepos(data chan string, wg *sync.WaitGroup, page int, token string, url string) {
	client := &http.Client{}
  perPage := "?per_page=100" + "&page=" + strconv.Itoa(page)
	req, err := http.NewRequest("GET", url + perPage, nil)
	if err != nil {
		log.Fatal(err)
	}
  setHeaders(req,token)
	resp, err := client.Do(req)
	if err != nil {
		log.Fatal(err)
	}

	defer resp.Body.Close()
  bodyText, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}
  data <- string(bodyText)
  wg.Done()
}
