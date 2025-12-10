import arxiv_downloader
import pdf_processor

def main():
    print("\n Hello! How can I help you today?")
    
    while True:
        print("\n Choose an option:")
        print("1 Download Research Papers")
        print("2 Retrieve information from existing papers")
        print("0 Exit")
        
        choice = input("Enter your choice (1/2/0): ").strip()
        
        if choice == "1":
            query = input("\n Enter the research topic: ").strip()
            arxiv_downloader.fetch_and_download_papers(query=query)
        
        elif choice == "2":
            while True:
                query = input('\n What do you want to ask? (Type "exit" to return to main menu): ').strip()
                if query.lower() == "exit":
                    break
                pdf_processor.process_query(query=query)

        elif choice == "0":
            print("\n Goodbye! Have a great day!")
            break
        
        else:
            print("\n Invalid choice. Please enter 1, 2, or 0.")

if __name__ == "__main__":
    main()
