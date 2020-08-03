# Python Web Scraping Test
## Author Novak Zaballa

### Usage

```
from gascrap import get_similar
print(get_similar('homedepot.com'))
```

Use get_similar(hostname) where hostname is string, to get a list of stores similar to hostname.
    Parameters
        hostname (string). A store hostname. 
    Outcome (JSON)
        This function will find and return stores in Giving Asssitance site 
        that are similar to the hostname provided as input. The result is 
        an array of 'hostname' and 'title' key value pairs in JSON format.

Aassumptions were: 
  - Since no additional information was provided, We can get the Similar Stores from the Similar Stores Coupons section of the store page in the Giving Assistance site.
  - The Script will run interactively. So I added a few prints and progress bar to offer feedback to the user about the progress, since its execution takes several minutes.
