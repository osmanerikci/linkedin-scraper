import pandas as pd
from preprocessing import preprocess_text
from lemmatization import lemmatize_text
from tfidf_analysis import extract_top_keywords
from scraping import scrape_linkedin_jobs

def main():
    # Scrape LinkedIn jobs
    jobs_data = scrape_linkedin_jobs()

    # Convert to DataFrame and save to Excel
    df = pd.DataFrame(jobs_data)
    df.to_excel('linkedin_jobs.xlsx', index=False)

    # Load the DataFrame
    df = pd.read_excel('linkedin_jobs.xlsx')

    # Preprocess text
    df['Description'] = df['Description'].apply(preprocess_text)

    # Lemmatize text
    df['Description'] = df['Description'].apply(lemmatize_text)

    # Extract top keywords
    top_keywords = extract_top_keywords(df['Description'])

    # Print top 20 keywords
    for word, score in top_keywords[:50]:
        print(f"{word}: {score:.4f}")

if __name__ == "__main__":
    main()
