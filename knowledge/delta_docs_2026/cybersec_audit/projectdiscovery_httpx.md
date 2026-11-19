# Official Delta Reference: projectdiscovery_httpx
Source: https://github.com/projectdiscovery/httpx
Domain: cybersec_audit

Title: GitHub - projectdiscovery/httpx: httpx is a fast and multi-purpose HTTP toolkit that allows running multiple probes using the retryablehttp library.

URL Source: https://github.com/projectdiscovery/httpx

Markdown Content:
## [![Image 1: httpx](https://github.com/projectdiscovery/httpx/raw/dev/static/httpx-logo.png)](https://github.com/projectdiscovery/httpx/blob/dev/static/httpx-logo.png)

[](https://github.com/projectdiscovery/httpx#----)

[![Image 2](https://camo.githubusercontent.com/0fddb38e25d5cf8660a916fc09691ba95201d60e309b6371d2b66ce9e6ce76ec/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c6963656e73652d4d49542d5f7265642e737667)](https://opensource.org/licenses/MIT)[![Image 3](https://camo.githubusercontent.com/b6bce8cc8d32e2c9c9ea33c44c0772be6d1a957b94259edc37343f7912a8b993/68747470733a2f2f676f7265706f7274636172642e636f6d2f62616467652f6769746875622e636f6d2f70726f6a656374646973636f766572792f6874747078)](https://goreportcard.com/badge/github.com/projectdiscovery/httpx)[![Image 4](https://camo.githubusercontent.com/85076242828fa6b8764a53867c88529755b9f914c1861eb44af00e4e5338c55e/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f72656c656173652f70726f6a656374646973636f766572792f6874747078)](https://github.com/projectdiscovery/httpx/releases)[![Image 5](https://camo.githubusercontent.com/3c0e4a5fcfce6f2e6f9db7cba987d916181a612f5e0de423304b14c320df4539/68747470733a2f2f696d672e736869656c64732e696f2f646f636b65722f70756c6c732f70726f6a656374646973636f766572792f68747470782e737667)](https://hub.docker.com/r/projectdiscovery/httpx)[![Image 6](https://camo.githubusercontent.com/2d0ee1231b5e86ebe0caf6f58d434000ab1a6dc87d8af12160d2a12e8ac63d27/68747470733a2f2f696d672e736869656c64732e696f2f747769747465722f666f6c6c6f772f70646973636f76657279696f2e7376673f6c6f676f3d74776974746572)](https://twitter.com/pdiscoveryio)[![Image 7](https://camo.githubusercontent.com/880e9bce17c3ec3a464728df4f8945d064295c0e9392ef4b815242eac78515ed/68747470733a2f2f696d672e736869656c64732e696f2f646973636f72642f3639353634353233373431383133313530372e7376673f6c6f676f3d646973636f7264)](https://discord.gg/projectdiscovery)

[Features](https://github.com/projectdiscovery/httpx#features) • [Installation](https://github.com/projectdiscovery/httpx#installation-instructions) • [Usage](https://github.com/projectdiscovery/httpx#usage) • [Documentation](https://docs.projectdiscovery.io/tools/httpx/) • [Notes](https://github.com/projectdiscovery/httpx#notes) • [Join Discord](https://discord.gg/projectdiscovery)

`httpx` is a fast and multi-purpose HTTP toolkit that allows running multiple probes using the [retryablehttp](https://github.com/projectdiscovery/retryablehttp-go) library. It is designed to maintain result reliability with an increased number of threads.

## Features

[](https://github.com/projectdiscovery/httpx#features)

## [![Image 8: httpx](https://user-images.githubusercontent.com/8293321/135731750-4c1d38b1-bd2a-40f9-88e9-3c4b9f6da378.png)](https://user-images.githubusercontent.com/8293321/135731750-4c1d38b1-bd2a-40f9-88e9-3c4b9f6da378.png)

[](https://github.com/projectdiscovery/httpx#-----1)

*   Simple and modular code base making it easy to contribute.
*   Fast And fully configurable flags to probe multiple elements.
*   Supports multiple HTTP based probings.
*   Smart auto fallback from https to http by default.
*   Supports hosts, URLs and CIDR as input.
*   Handles edge cases doing retries, backoffs etc for handling WAFs.

### Supported probes

[](https://github.com/projectdiscovery/httpx#supported-probes)
| Probes | Default check | Probes | Default check |
| --- | --- | --- | --- |
| URL | true | IP | true |
| Title | true | CNAME | true |
| Status Code | true | Raw HTTP | false |
| Content Length | true | HTTP2 | false |
| TLS Certificate | true | HTTP Pipeline | false |
| CSP Header | true | Virtual host | false |
| Line Count | true | Word Count | true |
| Location Header | true | CDN | false |
| Web Server | true | Paths | false |
| Web Socket | true | Ports | false |
| Response Time | true | Request Method | true |
| Favicon Hash | false | Probe Status | false |
| Body Hash | true | Header Hash | true |
| Redirect chain | false | URL Scheme | true |
| JARM Hash | false | ASN | false |

## Installation Instructions

[](https://github.com/projectdiscovery/httpx#installation-instructions)
`httpx` requires **go >=1.26.10** to install successfully. Run the following command to get the repo:

go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

To learn more about installing httpx, see [https://docs.projectdiscovery.io/tools/httpx/install](https://docs.projectdiscovery.io/tools/httpx/install).

| ❗ **Disclaimer** |
| --- |
| **This project is in active development**. Expect breaking changes with releases. Review the changelog before updating. |
| This project was primarily built to be used as a standalone CLI tool. **Running it as a service may pose security risks.** It's recommended to use with caution and additional security measures. |

## Usage

[](https://github.com/projectdiscovery/httpx#usage)

httpx -h

This will display help for the tool. Here are all the switches it supports.

httpx is a fast and multi-purpose HTTP toolkit that allows running multiple probes using the retryablehttp library.

Usage:
 ./httpx [flags]

Flags:
INPUT:
 -l, -list string input file containing list of hosts to process
 -rr, -request string file containing raw request
 -u, -target string[] input target host(s) to probe
 -im, -input-mode string mode of input file (burp)

PROBES:
 -sc, -status-code display response status-code
 -cl, -content-length display response content-length
 -ct, -content-type display response content-type
 -location display response redirect location
 -favicon display mmh3 hash for '/favicon.ico' file
 -hash string display response body hash (supported: md5,mmh3,simhash,sha1,sha256,sha512)
 -jarm display jarm fingerprint hash
 -rt, -response-time display response time
 -lc, -line-count display response body line count
 -wc, -word-count display response body word count
 -title display page title
 -bp, -body-preview display first N characters of response body (default 100)
 -server, -web-server display server name
 -td, -tech-detect display technology in use based on wappalyzer dataset
 -cff, -custom-fingerprint-file string path to a custom fingerprint file for technology detection
 -kb, -knowledge-base enable knowledge base classification
 -method display http request method
 -ws, -websocket display server using websocket
 -ip display host ip
 -cname display host cname
 -extract-fqdn, -efqdn get domain and subdomains from response body and header in jsonl/csv output
 -asn display host asn information
 -cdn display cdn/waf in use (default true)
 -probe display probe status

HEADLESS:
 -ss, -screenshot enable saving screenshot of the page using headless browser
 -system-chrome enable using local installed chrome for screenshot
 -ho, -headless-options string[] start headless chrome with additional options
 -esb, -exclude-screenshot-bytes enable excluding screenshot bytes from json output
 -ehb, -exclude-headless-body enable excluding headless header from json output
 -no-screenshot-full-page disable saving full page screenshot
 -st, -screenshot-timeout value set timeout for screenshot in seconds (default 10s)
 -sid, -screenshot-idle value set idle time before taking screenshot in seconds (default 1s)
 -jsc, -javascript-code string[] execute JavaScript code after navigation

MATCHERS:
 -mc, -match-code string match response with specified status code (-mc 200,302)
 -ml, -match-length string match response with specified content length (-ml 100,102)
 -mlc, -match-line-count string match response body with specified line count (-mlc 423,532)
 -mwc, -match-word-count string match response body with specified word count (-mwc 43,55)
 -mfc, -match-favicon string[] match response with specified favicon hash (-mfc 1494302000)
 -ms, -match-string string[] match response with specified string (-ms admin)
 -mr, -match-regex string[] match response with specified regex (-mr admin)
 -mcdn, -match-cdn string[] match host with specified cdn provider (cloudfront, fastly, google, etc.)
 -mrt, -match-response-time string match response with specified response time in seconds (-mrt '< 1')
 -mdc, -match-condition string match response with dsl expression condition

EXTRACTOR:
 -er, -extract-regex string[] display response content with matched regex
 -ep, -extract-preset string[] display response content matched by a pre-defined regex (url,ipv4,mail)

FILTERS:
 -fc, -filter-code string filter response with specified status code (-fc 403,401)
 -fpt, -filter-page-type string[] filter response with specified page type (e.g. -fpt login,captcha,parked)
 -fep, -filter-error-page [DEPRECATED: use -fpt] filter response with ML based error page detection
 -fd, -filter-duplicates filter out near-duplicate responses (only first response is retained)
 -fl, -filter-length string filter response with specified content length (-fl 23,33)
 -flc, -filter-line-count string filter response body with specified line count (-flc 423,532)
 -fwc, -filter-word-count string filter response body with specified word count (-fwc 423,532)
 -ffc, -filter-favicon string[] filter response with specified favicon hash (-ffc 1494302000)
 -fs, -filter-string string[] filter response with specified string (-fs admin)
 -fe, -filter-regex string[] filter response with specified regex (-fe admin)
 -fcdn, -filter-cdn string[] filter host with specified cdn provider (cloudfront, fastly, google, etc.)
 -frt, -filter-response-time string filter response with specified response time in seconds (-frt '> 1')
 -fdc, -filter-condition string filter response with dsl expression condition
 -strip strips all tags in response. supported formats: html,xml (default html)
 -lof, -list-output-fields list of fields to output (comma separated)
 -eof, -exclude-output-fields string[] exclude output fields output based on a condition

RATE-LIMIT:
 -t, -threads int number of threads to use (default 50)
 -rl, -rate-limit int maximum requests to send per second (default 150)
 -rlm, -rate-limit-minute int maximum number of requests to send per minute

MISCELLANEOUS:
 -pa, -probe-all-ips probe all the ips associated with same host
 -p, -ports string[] ports to probe (nmap syntax: eg http:1,2-10,11,https:80)
 -path string path or list of paths to probe (comma-separated, file)
 -tls-probe send http probes on the extracted TLS domains (dns_name)
 -csp-probe send http probes on the extracted CSP domains
 -tls-grab perform TLS(SSL) data grabbing
 -pipeline probe and display server supporting HTTP1.1 pipeline
 -http2 probe and display server supporting HTTP2
 -vhost probe and display server supporting VHOST
 -ldv, -list-dsl-variables list json output field keys name that support dsl matcher/filter

UPDATE:
 -up, -update update httpx to latest version
 -duc, -disable-update-check disable automatic httpx update check

OUTPUT:
 -o, -output string file to write output results
 -oa, -output-all filename to write output results in all formats
 -sr, -store-response store http response to output directory
 -srd, -store-response-dir string store http response to custom directory
 -ob, -omit-body omit response body in output
 -csv store output in csv format
 -csvo, -csv-output-encoding string define output encoding
 -j, -json store output in JSONL(ines) format
 -irh, -include-response-header include http response (headers) in JSON output (-json only)
 -irr, -include-response include http request/response (headers + body) in JSON output (-json only)
 -irrb, -include-response-base64 include base64 encoded http request/response in JSON output (-json only)
 -include-chain include redirect http chain in JSON output (-json only)
 -store-chain include http redirect chain in responses (-sr only)
 -svrc, -store-vision-recon-cluster include visual recon clusters (-ss and -sr only)
 -pr, -protocol string protocol to use (unknown, http11, http2, http3)
 -fepp, -filter-error-page-path string path to store filtered error pages (default "filtered_error_page.json")
 -rdb, -result-db store results in database
 -rdbc, -result-db-config string path to database config file
 -rdbt, -result-db-type string database type (mongodb, postgres, mysql)
 -rdbcs, -result-db-conn string database connection string (env: HTTPX_DB_CONNECTION_STRING)
 -rdbn, -result-db-name string database name (default "httpx")
 -rdbtb, -result-db-table string table/collection name (default "results")
 -rdbbs, -result-db-batch-size int batch size for database inserts (default 100)
 -rdbor, -result-db-omit-raw omit raw request/response data from database

CONFIGURATIONS:
 -config string path to the httpx configuration file (default $HOME/.config/httpx/config.yaml)
 -ptm, -page-type-model string path to a local dit model for page classification (requires -kb or -fpt; skips model download)
 -r, -resolvers string[] list of custom resolver (file or comma separated)
 -allow string[] allowed list of IP/CIDR's to process (file or comma separated)
 -deny string[] denied list of IP/CIDR's to process (file or comma separated)
 -sni, -sni-name string custom TLS SNI name
 -random-agent enable Random User-Agent to use (default true)
 -auto-referer set the Referer header to the current URL
 -H, -header string[] custom http headers to send with request
 -http-proxy, -proxy string proxy (http|socks) to use (eg http://127.0.0.1:8080)
 -unsafe send raw requests skipping golang normalization
 -resume resume scan using resume.cfg
 -fr, -follow-redirects follow http redirects
 -maxr, -max-redirects int max number of redirects to follow per host (default 10)
 -fhr, -follow-host-redirects follow redirects on the same host
 -rhsts, -respect-hsts respect HSTS response headers for redirect requests
 -vhost-input get a list of vhosts as input
 -x string request methods to probe, use 'all' to probe all HTTP methods
 -body string post body to include in http request
 -s, -stream stream mode - start elaborating input targets without sorting
 -sd, -skip-dedupe disable dedupe input items (only used with stream mode)
 -ldp, -leave-default-ports leave default http/https ports in host header (eg. http://host:80 - https://host:443
 -ztls use ztls library with autofallback to standard one for tls13
 -no-decode avoid decoding body
 -tlsi, -tls-impersonate string enable experimental client hello (ja3) tls impersonation (chrome, or ja3 full string)
 -no-stdin Disable Stdin processing
 -hae, -http-api-endpoint string experimental http api endpoint
 -sf, -secret-file string path to secret file for authentication

DEBUG:
 -health-check, -hc run diagnostic check up
 -debug display request/response content in cli
 -debug-req display request content in cli
 -debug-resp display response content in cli
 -version display httpx version
 -stats display scan statistic
 -profile-mem string optional httpx memory profile dump file
 -silent silent mode
 -v, -verbose verbose mode
 -si, -stats-interval int number of seconds to wait between showing a statistics update (default: 5)
 -mp, -metrics-port int port to expose httpx metrics on (default 63636)
 -nc, -no-color disable colors in cli output
 -tr, -trace trace

OPTIMIZATIONS:
 -nf, -no-fallback display both probed protocol (HTTPS and HTTP)
 -nfs, -no-fallback-scheme probe with protocol scheme specified in input
 -maxhr, -max-host-error int max error count per host before skipping remaining path/s (default 30)
 -e, -exclude string[] exclude host matching specified filter ('cdn', 'private-ips', cidr, ip, regex)
 -retries int number of retries
 -timeout int timeout in seconds (default 10)
 -delay value duration between each http request (eg: 200ms, 1s) (default -1ns)
 -rsts, -response-size-to-save int max response size to save in bytes (default 50000000)
 -rstr, -response-size-to-read int max response size to read in bytes (default 50000000)

CLOUD:
 -auth configure projectdiscovery cloud (pdcp) api key (default true)
 -ac, -auth-config string configure projectdiscovery cloud (pdcp) api key credential file
 -pd, -dashboard upload / view output in projectdiscovery cloud (pdcp) UI dashboard
 -tid, -team-id string upload asset results to given team id (optional)
 -aid, -asset-id string upload new assets to existing asset id (optional)
 -aname, -asset-name string assets group name to set (optional)
 -pdu, -dashboard-upload string upload httpx output file (jsonl) in projectdiscovery cloud (pdcp) UI dashboard

For details about running httpx, see [https://docs.projectdiscovery.io/tools/httpx/running](https://docs.projectdiscovery.io/tools/httpx/running).

### Using `httpx` as a library

[](https://github.com/projectdiscovery/httpx#using-httpx-as-a-library)
`httpx` can be used as a library by creating an instance of the `Option` struct and populating it with the same options that would be specified via CLI. Once validated, the struct should be passed to a runner instance (to be closed at the end of the program) and the `RunEnumeration` method should be called. A minimal example of how to do it is in the [examples](https://github.com/projectdiscovery/httpx/blob/dev/examples) folder.

### Using a local page classification model

[](https://github.com/projectdiscovery/httpx#using-a-local-page-classification-model)
For environments that cannot reach Hugging Face, provision the [dit model.json](https://huggingface.co/datasets/happyhackingspace/dit/resolve/main/model.json) on an accessible machine and copy it to the scanning environment. Select it with `-page-type-model` (`-ptm`):

httpx -l hosts.txt -kb -json -ptm /opt/httpx/model.json
httpx -l hosts.txt -fpt error,parked -ptm /opt/httpx/model.json

The path selects a local model and bypasses automatic model discovery and downloading. A missing or unreadable model, or invalid model JSON, stops initialization instead of falling back to a download. Classification remains opt-in: use `-kb` or `-fpt` (the deprecated `-fep` is also supported). Setting `-ptm` alone does not load the model or enable classification. Library users can set `Options.PageTypeModel` alongside `KnowledgeBase` or `OutputFilterPageType`. Without a custom path, the existing model discovery and download behavior is unchanged.

Explicit models must also pass a page and form classification check before scanning starts or existing output indexes are changed. This checks that the model can run, rather than certifying every part of its contents. A later classification error leaves that response without page-type information; diagnostics are available with `-debug`.

## Common Recipes

[](https://github.com/projectdiscovery/httpx#common-recipes)
Below are practical one-liners for common use cases leveraging httpx's composable primitives. These recipes are validated in `runner/wellknown_recipes_test.go`.

Use `-mdc` with DSL helpers such as `contains(content_type, ...)` and `contains(body, ...)` to match response metadata and body content. (`-mr`/`-ms` match the full raw response; use `-mdc` for structured field matching.)

### Well-known files

[](https://github.com/projectdiscovery/httpx#well-known-files)
**security.txt**  
 Probe for a valid [RFC 9116](https://www.rfc-editor.org/rfc/rfc9116.html) security.txt file at the standard paths (`/.well-known/security.txt`, `/security.txt`):

echo target.com | httpx -path '/.well-known/security.txt,/security.txt' -mc 200 -mdc 'contains(content_type, "text/plain") && contains(body, "Contact:") && contains_any(body, "mailto:", "https://")'

*   `-path` tests custom path(s)
*   `-mc 200` matches HTTP 200
*   `-mdc` matches using DSL expressions on response fields such as `content_type` and `body`

**robots.txt**

echo target.com | httpx -path '/robots.txt' -mc 200 -mdc 'contains(content_type, "text/plain")'

**sitemap.xml**

echo target.com | httpx -path '/sitemap.xml' -mc 200 -mdc 'contains_any(content_type, "application/xml", "text/xml") && contains(body, "<urlset")'

**humans.txt**

echo target.com | httpx -path '/humans.txt' -mc 200 -mdc 'contains(content_type, "text/plain")'

**ads.txt**

echo target.com | httpx -path '/ads.txt' -mc 200 -mdc 'contains(content_type, "text/plain") && contains(body, "google.com")'

### Well-known URIs

[](https://github.com/projectdiscovery/httpx#well-known-uris)
**OpenID Connect discovery** ([spec](https://openid.net/specs/openid-connect-discovery-1_0.html))

echo target.com | httpx -path '/.well-known/openid-configuration' -mc 200 -mdc 'contains(content_type, "application/json") && contains(body, "\"issuer\"")'

**Apple Universal Links**

echo target.com | httpx -path '/.well-known/apple-app-site-association,/.well-known/apple-app-site-association.json' -mc 200 -mdc 'contains(content_type, "application/json") && contains(body, "\"applinks\"")'

**Android App Links**

echo target.com | httpx -path '/.well-known/assetlinks.json' -mc 200 -mdc 'contains(content_type, "application/json") && contains(body, "\"android_app\"")'

**crossdomain.xml** (legacy Flash policy file)

echo target.com | httpx -path '/crossdomain.xml' -mc 200 -mdc 'contains_any(content_type, "application/xml", "text/xml") && contains(body, "cross-domain-policy")'

**Other well-known URIs** ([IANA registry](https://www.iana.org/assignments/well-known-uris/well-known-uris.xhtml)):

echo target.com | httpx -path '/.well-known/security.txt,/.well-known/change-password,/.well-known/openid-configuration' -mc 200

## Notes

[](https://github.com/projectdiscovery/httpx#notes)
*   As default, `httpx` probe with **HTTPS** scheme and fall-back to **HTTP** only if **HTTPS** is not reachable.
*   Burp Suite XML exports can be used as input with `-l burp-export.xml -im burp`
*   A target can be pinned to an IP with a JSON input line, in the format of nuclei target lines, like `curl --resolve` but on every port of its host: ```
{"target": "https://app.example.com", "ip": "192.0.2.10"}
{"target": "https://app.example.com", "ip": "192.0.2.11"}
``` 
    *   Every connection to the hostname, redirects included, goes to the IP, which `host_ip` reports and the output shows. The hostname is kept for the Host header and SNI and is not resolved. A host can be listed with several IPs, and a line without `ip` is the plain target.
    *   The keys nuclei uses to select templates, such as `tags`, are ignored, and any other key makes the line invalid. An invalid line is reported and skipped. The `input` of a result is the line in a canonical form.
    *   `-u` splits its value on commas, so pass such lines in a file (`-l`) or on stdin.
    *   A line with an IP stops the run with `-proxy`, `-pr http2`, `-unsafe`, `-pipeline`, `-http2`, `-jarm`, `-screenshot` and `-vhost-input`, as they do not connect through the IP or, for HTTP/2, share a connection between the IPs of a host. A proxy set with `HTTP_PROXY`/`HTTPS_PROXY` resolves the host itself too, so a probe through it fails: add the pinned hosts to `NO_PROXY`.
    *   `-pa` probes each IP of a host the same way, so it cannot be used with `-proxy` either. The IPs of a host are kept apart: `-maxhr` counts their failures and `-sr` stores their responses separately.
    *   Hostnames found by `-tls-probe` and `-csp-probe`, the pinned one included, are probed as new targets and resolved.

*   The `-no-fallback` flag can be used to probe and display both **HTTP** and **HTTPS** result.
*   Custom scheme for ports can be defined, for example `-ports http:443,http:80,https:8443`
*   Custom resolver supports multiple protocol (**doh|tcp|udp**) in form of `protocol:resolver:port` (e.g. `udp:127.0.0.1:53`)
*   Secret files can be used for domain-based authentication via `-sf secrets.yaml`. Supported auth types: `BasicAuth`, `BearerToken`, `Header`, `Cookie`, `Query`. Example: id: example-auth
info:
  name: Example Auth Config
static:
  - type: Header
    domains:
      - api.example.com
    headers:
      - key: X-API-Key
      