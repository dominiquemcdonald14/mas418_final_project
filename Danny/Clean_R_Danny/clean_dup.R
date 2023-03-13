library(tidyverse)

### Input file
setwd("/Users/tixradmin/Documents/GitHub/mas418_final_project/Glassdoor/output")
job_data <- read.csv("output_.csv")

### Cleaning
job_no_dup <- data.frame()
job_no_dup <- rbind(job_no_dup, job_data[1,])

for (i in 1:nrow(job_data)) {
  temp <- job_data[i,]
  
  check <- rbind(job_no_dup, temp) %>%
    select(-requested_url) %>%
    group_by(companyName, company_offeredRole, company_roleLocation, company_salary) %>%
    summarise(count = n())
  
  if (mean(check$count) == 1) {
    job_no_dup <- rbind(job_no_dup, job_data[i,])
  }
}

### Output file
setwd("/Users/tixradmin/Documents/GitHub/mas418_final_project/Glassdoor/output")
write.csv(job_no_dup, "output_.csv")