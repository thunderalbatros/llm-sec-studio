# Official Delta Reference: projectdiscovery_nuclei
Source: https://github.com/projectdiscovery/nuclei
Domain: cybersec_audit

Title: GitHub - projectdiscovery/nuclei: Nuclei is a fast, customizable vulnerability scanner powered by the global security community and built on a simple YAML-based DSL, enabling collaboration to tackle trending vulnerabilities on the internet. It helps you find vulnerabilities in your applications, APIs, networks, DNS, and cloud configurations.

URL Source: https://github.com/projectdiscovery/nuclei

Markdown Content:
[![Image 1: nuclei](https://github.com/projectdiscovery/nuclei/raw/dev/static/nuclei-cover-image.png)](https://github.com/projectdiscovery/nuclei/blob/dev/static/nuclei-cover-image.png)

[![Image 2](https://camo.githubusercontent.com/59c90e635765dec11773c321f76bb6d981b43d653e77954375cf8e350b002e87/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f63756d656e746174696f6e2d2532333030303030302e7376673f7374796c653d666f722d7468652d6261646765266c6f676f3d646174613a696d6167652f7376672b786d6c3b6261736536342c50484e325a79423462577875637a30696148523063446f764c336433647935334d793576636d63764d6a41774d43397a646d6369494864705a48526f505349794e434967614756705a326830505349794e434967646d6c6c64304a76654430694d43417749444930494449304969426d6157787350534a756232356c4969427a64484a766132553949694e6d5a6d5a6d5a6d596949484e30636d39725a53313361575230614430694d694967633352796232746c4c577870626d566a59584139496e4a766457356b4969427a64484a766132557462476c755a57707661573439496e4a766457356b4969426a6247467a637a30696248566a6157526c4947783159326c6b5a533169623239724c5739775a573469506a78775958526f49475139496b30784d694133646a45304969382b50484268644767675a44306954544d674d5468684d534178494441674d4341784c5445744d565930595445674d534177494441674d5341784c54466f4e574530494451674d434177494445674e434130494451674e434177494441674d5341304c54526f4e574578494445674d434177494445674d534178646a457a595445674d534177494441674d5330784944466f4c545a684d79417a494441674d4341774c544d674d79417a49444d674d434177494441744d79307a65694976506a777663335a6e50673d3d266c6f676f436f6c6f723d7768697465)](https://docs.projectdiscovery.io/tools/nuclei/overview?utm_source=github&utm_medium=web&utm_campaign=nuclei_readme)[![Image 3](https://camo.githubusercontent.com/3c9cd45bb9eac1d34499c5f22f454344296d6cfab893b81220f32cc3f34e12db/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f54656d706c61746573204c6962726172792d2532333030303030302e7376673f7374796c653d666f722d7468652d6261646765266c6f676f3d646174613a696d6167652f7376672b786d6c3b6261736536342c50484e325a79423462577875637a30696148523063446f764c336433647935334d793576636d63764d6a41774d43397a646d6369494864705a48526f505349784e694967614756705a326830505349784e694967646d6c6c64304a76654430694d43417749444930494449304969426d6157787350534a756232356c4969427a64484a766132553949694e6d5a6d5a6d5a6d596949484e30636d39725a53313361575230614430694d5334314969427a64484a766132557462476c755a574e6863443069636d3931626d516949484e30636d39725a5331736157356c616d3970626a3069636d3931626d516949474e7359584e7a50534a7364574e705a4755676248566a6157526c4c584e6f615756735a43492b50484268644767675a443069545449774944457a597a41674e53307a4c6a55674e7934314c5463754e6a59674f4334354e574578494445674d434177494445744c6a59334c5334774d554d334c6a55674d6a41754e53413049444534494451674d544e574e6d4578494445674d434177494445674d533078597a49674d4341304c6a55744d533479494459754d6a51744d6934334d6d45784c6a4533494445754d5463674d434177494445674d5334314d694177517a45304c6a557849444d754f4445674d5463674e5341784f534131595445674d534177494441674d534178494446364969382b5043397a646d632b266c6f676f436f6c6f723d7768697465)](https://github.com/projectdiscovery/nuclei-templates)[![Image 4](https://camo.githubusercontent.com/13a5d8503d1005afa86fab4bbb6b20539fab21510b8c29c1350ac014a1baae2e/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446973636f72642d2532333538363546322e7376673f7374796c653d666f722d7468652d6261646765266c6f676f3d646973636f7264266c6f676f436f6c6f723d7768697465)](https://discord.gg/projectdiscovery?utm_source=github&utm_medium=web&utm_campaign=nuclei_readme)

* * *

**Nuclei is a modern, high-performance vulnerability scanner that leverages simple YAML-based templates. It empowers you to design custom vulnerability detection scenarios that mimic real-world conditions, leading to zero false positives.**

*   Simple YAML format for creating and customizing vulnerability templates.
*   Contributed by thousands of security professionals to tackle trending vulnerabilities.
*   Reduce false positives by simulating real-world steps to verify a vulnerability.
*   Ultra-fast parallel scan processing and request clustering.
*   Integrate into CI/CD pipelines for vulnerability detection and regression testing.
*   Supports multiple protocols like TCP, DNS, HTTP, SSL, WHOIS, JavaScript, Code and more.
*   Integrate with Jira, Splunk, GitHub, Elastic, GitLab.

## Table of Contents

[](https://github.com/projectdiscovery/nuclei#table-of-contents)
*   [**`Get Started`**](https://github.com/projectdiscovery/nuclei#get-started)
    *   [_`1. Nuclei CLI`_](https://github.com/projectdiscovery/nuclei#1-nuclei-cli)
    *   [_`2. Pro and Enterprise Editions`_](https://github.com/projectdiscovery/nuclei#2-pro-and-enterprise-editions)

*   [**`Documentation`**](https://github.com/projectdiscovery/nuclei#documentation)
    *   [_`Command Line Flags`_](https://github.com/projectdiscovery/nuclei#command-line-flags)
    *   [_`Single target scan`_](https://github.com/projectdiscovery/nuclei#single-target-scan)
    *   [_`Scanning multiple targets`_](https://github.com/projectdiscovery/nuclei#scanning-multiple-targets)
    *   [_`Network scan`_](https://github.com/projectdiscovery/nuclei#network-scan)
    *   [_`Scanning with your custom template`_](https://github.com/projectdiscovery/nuclei#scanning-with-your-custom-template)
    *   [_`Connect Nuclei to ProjectDiscovery\_`_](https://github.com/projectdiscovery/nuclei#connect-nuclei-to-projectdiscovery)

*   [**`Nuclei Templates, Community and Rewards`**](https://github.com/projectdiscovery/nuclei#nuclei-templates-community-and-rewards-) 💎
*   [**`Our Mission`**](https://github.com/projectdiscovery/nuclei#our-mission)
*   [**`Contributors`**](https://github.com/projectdiscovery/nuclei#contributors-heart) ❤
*   [**`License`**](https://github.com/projectdiscovery/nuclei#license)

## Get Started

[](https://github.com/projectdiscovery/nuclei#get-started)
### **1. Nuclei CLI**

[](https://github.com/projectdiscovery/nuclei#1-nuclei-cli)
_Install Nuclei on your machine. Get started by following the installation guide [**`here`**](https://docs.projectdiscovery.io/tools/nuclei/install?utm\_source=github&utm\_medium=web&utm\_campaign=nuclei\_readme). Additionally, we provide [**`a free cloud tier`**](https://cloud.projectdiscovery.io/sign-up) that comes with generous monthly free limits:_

*   Store and visualize your vulnerability findings
*   Write and manage your Nuclei templates
*   Access the latest Nuclei templates
*   Discover and store your targets

Important

| **This project is in active development**. Expect breaking changes with releases. Review the release changelog before updating. |
| --- |
| This project is primarily built to be used as a standalone CLI tool. **Running nuclei as a service may pose security risks.** It's recommended to use with caution and additional security measures. |

### **2. Pro and Enterprise Editions**

[](https://github.com/projectdiscovery/nuclei#2-pro-and-enterprise-editions)
_For security teams and enterprises, we provide a cloud-hosted service built on top of Nuclei OSS, fine-tuned to help you continuously run vulnerability scans at scale with your team and existing workflows:_

*   50x faster scans
*   Large scale scanning with high accuracy
*   Integrations with cloud services (AWS, GCP, Azure, Cloudflare, Fastly, Terraform, Kubernetes)
*   Jira, Slack, Linear, APIs and Webhooks
*   Executive and compliance reporting
*   Plus: Real-time scanning, SAML SSO, SOC 2 compliant platform (with EU and US hosting options), shared team workspaces, and more
*   We're constantly [**`adding new features`**](https://feedback.projectdiscovery.io/changelog)!
*   **Ideal for:** Pentesters, security teams, and enterprises

[**`Sign up to Pro`**](https://projectdiscovery.io/pricing?utm_source=github&utm_medium=web&utm_campaign=nuclei_readme) or [**`Talk to our team`**](https://projectdiscovery.io/request-demo?utm_source=github&utm_medium=web&utm_campaign=nuclei_readme) if you have a large organization and complex requirements.

## Documentation

[](https://github.com/projectdiscovery/nuclei#documentation)
Browse the full Nuclei [**`documentation here`**](https://docs.projectdiscovery.io/tools/nuclei/running). If you’re new to Nuclei, check out our [**`foundational YouTube series`**](https://www.youtube.com/playlist?list=PLZRbR9aMzTTpItEdeNSulo8bYsvil80Rl).

[![Image 5](https://github.com/projectdiscovery/nuclei/raw/dev/static/nuclei-getting-started.png)](https://www.youtube.com/watch?v=b5qMyQvL1ZA&list=PLZRbR9aMzTTpItEdeNSulo8bYsvil80Rl&utm_source=github&utm_medium=web&utm_campaign=nuclei_readme)[![Image 6](https://github.com/projectdiscovery/nuclei/raw/dev/static/nuclei-write-your-first-template.png)](https://www.youtube.com/watch?v=nFXygQdtjyw&utm_source=github&utm_medium=web&utm_campaign=nuclei_readme)

### Installation

[](https://github.com/projectdiscovery/nuclei#installation)
`nuclei` requires **go >= 1.27.3** to install successfully. Run the following command to get the repo:

go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

To learn more about installing nuclei, see `https://docs.projectdiscovery.io/tools/nuclei/install`.

### Command Line Flags

[](https://github.com/projectdiscovery/nuclei#command-line-flags)
To display all the flags for the tool:

nuclei -h

Expand full help flags

Nuclei is a fast, template based vulnerability scanner focusing
on extensive configurability, massive extensibility and ease of use.

Usage:
  ./nuclei [flags]

Flags:
TARGET:
   -u, -target string[] target URLs/hosts to scan
   -l, -list string path to file containing a list of target URLs/hosts to scan (one per line)
   -targets-inline string inline multiline target list (for use in template profiles)
   -eh, -exclude-hosts string[] hosts to exclude to scan from the input list (ip, cidr, hostname)
   -resume string resume scan from and save to specified file (clustering will be disabled)
   -sa, -scan-all-ips scan all the IP's associated with dns record
   -iv, -ip-version string[] IP version to scan of hostname (4,6); default uses dialer fallback, -sa scans all addresses
   -dun, -disable-url-normalization keep targets exactly as supplied instead of collapsing urls that address the same resource
   -mup, -max-urls-per-pattern int scan at most this many urls sharing one structural shape, e.g. /user/1 and /user/2 (0 to scan all)

TARGET-FORMAT:
   -im, -input-mode string mode of input file (list, burp, har, jsonl, yaml, openapi, swagger, http) (default "list")
   -ro, -required-only use only required fields in input format when generating requests
   -sfv, -skip-format-validation skip format validation (like missing vars) when parsing input file
   -vtt, -vars-text-templating enable text templating for vars in input file (only for yaml input mode)
   -vfp, -var-file-paths string[] list of yaml file contained vars to inject into yaml input

TEMPLATES:
   -nt, -new-templates run only new templates added in latest nuclei-templates release
   -ntv, -new-templates-version string[] run new templates added in specific version
   -as, -automatic-scan automatic web scan using wappalyzer technology detection to tags mapping
   -auto-tech run the tech templates first, then skip templates bound to products they did not detect on the target
   -t, -templates string[] list of template or template directory to run (comma-separated, file)
   -turl, -template-url string[] template url or list containing template urls to run (comma-separated, file)
   -ai, -prompt string generate and run template using ai prompt
   -w, -workflows string[] list of workflow or workflow directory to run (comma-separated, file)
   -wurl, -workflow-url string[] workflow url or list containing workflow urls to run (comma-separated, file)
   -validate validate the passed templates to nuclei
   -plan string write the work a scan would do with its estimated cost to a jsonl file, then exit without sending requests to any target
   -run-plan string run only the entries of a -plan file, logging finished ones to <file>.done so running it again resumes, and following entries appended to it and ids appended to <file>.cancel
   -nss, -no-strict-syntax disable strict syntax check on templates
   -td, -template-display displays the templates content
   -tl list all templates matching current filters
   -tgl list all available tags
   -sign signs the templates with the private key defined in NUCLEI_SIGNATURE_PRIVATE_KEY env variable
   -code enable loading code protocol-based templates
   -dut, -disable-unsigned-templates disable running unsigned templates or templates with mismatched signature
   -esc, -enable-self-contained enable loading self-contained templates
   -egm, -enable-global-matchers enable loading global matchers templates
   -file enable loading file templates
   -llm enable llm matchers and extractors (semantic matching)
   -llm-provider string llm provider for semantic matching (openai, ollama, llamacpp, vllm, lmstudio, groq, openrouter, together, orcarouter, jev) (default "openai")
   -llm-base-url string openai-compatible endpoint for semantic matching (overrides -llm-provider, e.g. a local model)
   -llm-model string model used for semantic matching
   -llm-timeout int time in seconds to wait for a single llm call (default 30)
   -llm-max-calls int maximum llm calls per scan (0 for unlimited) (default 5000)
   -llm-concurrency int maximum concurrent llm calls (default 4)
   -llm-cache cache llm responses within a scan (default true)

FILTERING:
   -a, -author string[] templates to run based on authors (comma-separated, file)
   -tags string[] templates to run based on tags (comma-separated, file)
   -etags, -exclude-tags string[] templates to exclude based on tags (comma-separated, file)
   -itags, -include-tags string[] tags to be executed even if they are excluded either by default or configuration
   -id, -template-id string[] templates to run based on template ids (comma-separated, file, allow-wildcard)
   -eid, -exclude-id string[] templates to exclude based on template ids (comma-separated, file)
   -it, -include-templates string[] path to template file or directory to be executed even if they are excluded either by default or configuration
   -et, -exclude-templates string[] path to template file or directory to exclude (comma-separated, file)
   -em, -exclude-matchers string[] template matchers to exclude in result
   -s, -severity value[] templates to run based on severity. Possible values: info, low, medium, high, critical, unknown
   -es, -exclude-severity value[] templates to exclude based on severity. Possible values: info, low, medium, high, critical, unknown
   -pt, -type value[] templates to run based on protocol type. Possible values: dns, file, http, headless, tcp, workflow, ssl, websocket, whois, code, javascript
   -ept, -exclude-type value[] templates to exclude based on protocol type. Possible values: dns, file, http, headless, tcp, workflow, ssl, websocket, whois, code, javascript
   -tc, -template-condition string[] templates to run based on expression condition

OUTPUT:
   -o, -output string output file to write found issues/vulnerabilities
   -sresp, -store-resp store all request/response passed through nuclei to output directory
   -srd, -store-resp-dir string store all request/response passed through nuclei to custom directory (default "output")
   -store-events string store what the matchers of every request see, for any protocol, to a jsonl file for -replay (holds raw traffic, credentials included)
   -silent display findings only
   -nc, -no-color disable output content coloring (ANSI escape codes)
   -j, -jsonl write output in JSONL(ines) format
   -irr, -include-rr -omit-raw include request/response pairs in the JSON, JSONL, and Markdown outputs (for findings only) [DEPRECATED use -omit-raw] (default true)
   -or, -omit-raw omit request/response pairs in the JSON, JSONL, and Markdown outputs (for findings only)
   -ot, -omit-template omit encoded template in the JSON, JSONL output
   -nm, -no-meta disable printing result metadata in cli output
   -ts, -timestamp enables printing timestamp in cli output
   -rdb, -report-db string nuclei reporting database (always use this to persist report data)
   -ms, -matcher-status display match failure status
   -me, -markdown-export string directory to export results in markdown format
   -se, -sarif-export string file to export results in SARIF format
   -je, -json-export string file to export results in JSON format
   -jle, -jsonl-export string file to export results in JSONL(ine) format
   -ce, -csv-export string file to export results in CSV format
   -pe, -pdf-export string file to export results in PDF format
   -rd, -redact string[] redact given list of keys from query parameter, request header and body
   -nrd, -no-redact disable the built-in redaction of credential headers (Authorization, Cookie, Set-Cookie, ...) in output; keys given with -redact are still redacted

CONFIGURATIONS:
   -config string path to the nuclei configuration file
   -tp, -profile string template profile config file to run
   -tpl, -profile-list list community template profiles
   -fr, -follow-redirects enable following redirects for http templates
   -fhr, -follow-host-redirects follow redirects on the same host
   -mr, -max-redirects int max number of redirects to follow for http templates (default 10)
   -dr, -disable-redirects disable redirects for http templates
   -rc, -report-config string nuclei reporting module configuration file
   -H, -header string[] custom header/cookie to include in all http request in header:value format (cli, file)
   -V, -var value custom vars in key=value format
   -r, -resolvers string file containing resolver list for nuclei
   -sr, -system-resolvers use system DNS resolving as error fallback
   -dc, -disable-clustering disable clustering of requests
   -passive enable passive HTTP response processing mode
   -replay string run the templates' matchers and extractors over a -store-events file and print the findings sorted, without sending requests
   -fh2, -force-http2 force http2 connection on requests
   -ev, -env-vars enable environment variables to be used in template
   -cc, -client-cert string client certificate file (PEM-encoded) used for authenticating against scanned hosts
   -ck, -client-key string client key file (PEM-encoded) used for authenticating against scanned hosts
   -ca, -client-ca string client certificate authority file (PEM-encoded) used for authenticating against scanned hosts
   -sml, -show-match-line show match lines for file templates, works with extractors only
   -ztls use ztls library with autofallback to standard one for tls13 [Deprecated] autofallback to ztls is enabled by default
   -sni string tls sni hostname to use (default: input domain name)
   -dka, -dialer-keep-alive value keep-alive duration for network requests.
   -lfa, -allow-local-file-access allow all templates in the run to read any file on the system (not just payloads)
   -lna, -restrict-local-network-access blocks connections to the local / private network
   -i, -interface string network interface to use for network scan
   -at, -attack-type string type of payload combinations to perform (batteringram,pitchfork,clusterbomb)
   -pro, -payload-random-order iterate payload combinations in a random order instead of sequentially
   -sip, -source-ip string source ip address to use for network scan
   -rsr, -response-size-read int max response size to read in bytes
   -rss, -response-size-save int max response size to read in bytes (default 1048576)
   -rqss, -request-size-save int max request body size to save in bytes (0 to save the whole body) (default 32768)
   -mrbi, -max-request-body-inflight int max request body bytes held by in-flight http requests; requests with bodies of 1MB or more queue past it (0 disables)
   -reset reset removes all nuclei configuration and data files (including nuclei-templates)
   -tlsi, -tls-impersonate enable experimental client hello (ja3) tls randomization
   -hae, -http-api-endpoint string experimental http api endpoint

INTERACTSH:
   -iserver, -interactsh-server string interactsh server url for self-hosted instance (default: oast.pro,oast.live,oast.site,oast.online,oast.fun,oast.me)
   -itoken, -interactsh-token string authentication token for self-hosted interactsh server
   -interactions-cache-size int number of requests to keep in the interactions cache (default 5000)
   -interactions-eviction int number of seconds to wait before evicting requests from cache (default 60)
   -interactions-poll-duration int number of seconds to wait before each interaction poll request (default 5)
   -interactions-cooldown-period int extra time for interaction polling before exiting (default 5)
   -ni, -no-interactsh disable interactsh server for OAST testing, exclude OAST based templates

FUZZING:
   -ft, -fuzzing-type string overrides fuzzing type set in template (replace, prefix, postfix, infix)
   -fm, -fuzzing-mode string overrides fuzzing mode set in template (multiple, single)
   -fuzz enable loading fuzzing templates (Deprecated: use -dast instead)
   -dast enable / run dast (fuzz) nuclei templates
   -dts, -dast-server enable dast server mode (live fuzzing)
   -dtr, -dast-report write dast scan report to file
   -dtst, -dast-server-token string dast server token (optional)
   -dtsa, -dast-server-address string dast server address (default "localhost:9055")
   -dtp, -dast-proxy enable dast proxy mode (fuzz live traffic proxied through nuclei)
   -dtpa, -dast-proxy-address string dast proxy listen address (default "127.0.0.1:9056")
   -dtpau, -dast-proxy-auth string dast proxy basic auth in user:pass format (required for non-loopback address)
   -dfp, -display-fuzz-points display fuzz points in the output for debugging
   -fuzz-param-frequency int frequency of uninteresting parameters for fuzzing before skipping (default 10)
   -fa, -fuzz-aggression string fuzzing aggression level controls payload count for fuzz (low, medium, high) (default "low")
   -cs, -fuzz-scope string[] in scope url regex to be followed by fuzzer
   -cos, -fuzz-out-scope string[] out of scope url regex to be excluded by fuzzer

UNCOVER:
   -uc, -uncover enable uncover engine
   -uq, -uncover-query string[] uncover search query
   -ue, -uncover-engine string[] uncover search engine (shodan,censys,fofa,shodan-idb,quake,hunter,zoomeye,netlas,criminalip,publicwww,hunterhow,google) (default shodan)
   -uf, -uncover-field string uncover fields to return (ip,port,host) (default "ip:port")
   -ul, -uncover-limit int uncover results to return (default 100)
   -ur, -uncover-ratelimit int override ratelimit of engines with unknown ratelimit (default 60 req/min) (default 60)

RATE-LIMIT:
   -rl, -rate-limit int maximum number of requests to send per second (default 150)
   -rld, -rate-limit-duration value maximum number of requests to send per second (default 1s)
   -host-backoff slow down a host that starts blocking (429, repeated 403s, connection failures)
   -host-backoff-max value maximum delay applied to a host that is blocking (default 30s)
   -per-host-rate-limit enable per-host rate limiting (global rate limit becomes unlimited when enabled)
   -rlm, -rate-limit-minute int maximum number of requests to send per minute (DEPRECATED)
   -bs, -bulk-size int maximum number of hosts to be analyzed in parallel per template (default 25)
   -c, -concurrency int maximum number of templates to be executed in p