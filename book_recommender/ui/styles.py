MAIN_STYLES = """
<style>
    .header {
        text-align: center;
        padding: 1.5rem 0;
    }
    .header.h1 {
        text-align: center;
        margin-bottom: 1.5rem;
    }

    .header.h1 h1 {
        margin-bottom: 0.3rem;
    }

    .header .subtitle {
        font-size: 1.1rem;
        color: #666;
    }

    .book-card { 
        border-radius: 5px; 
        padding: 5px;
        transition: transform 0.3s, box-shadow 0.3s;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        background-color: white;
        height: 450px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .book-card:hover { 
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .book-card img {
        max-height: 180px;
        object-fit: contain;
        border-radius: 4px;
    }
    .section-title { 
        border-bottom: 2px solid #4f8bf9; 
        padding-bottom: 0.5rem; 
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .compact-header { 
        display: flex; 
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
        padding: 0.5rem 1rem;
        background-color: #f8f9fa;
        border-radius: 10px;
    }
    .book-title {
        font-weight: 500;
        font-size: 1.1rem;
        color: #f39c12;
        margin: 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .recommendation-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 0.5rem;
        padding: 0.75rem 1rem;
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        border-radius: 8px;
    }
    .selection-row {
        display: flex;
        gap: 1rem;
        align-items: center;
        margin: 0.5rem 0;
    }
    .book-chip {
        background-color: #e3f2fd;
        color: #1976d2;
        border-radius: 16px;
        padding: 0.25rem 0.75rem;
        font-size: 0.85rem;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
    }
    .book-details {
        font-size: 0.8rem;
        color: #666;
        text-align: center;
        margin-top: 5px;
    }
    .book-cover-placeholder {
        height: 220px;
        width: 150px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #f0f0f0;
        color: #333;
        font-size: 0.9rem;
        text-align: center;
        padding: 0.5rem;
        border-radius: 4px;
        word-wrap: break-word;
    }
    /* NEW styles moved from inline */

    .header.h1-container {
        text-align: center; 
        margin-bottom: 2rem;
    }

    .book-card .image-container {
        display: flex; 
        justify-content: center; 
        margin-bottom: 10px;
    }

    .book-card .title {
        font-size: 0.95rem; 
        text-align: center; 
        margin-top: 5px;
    }

    .book-card .genre {
        font-size: 0.85rem; 
        text-align: center; 
        margin-top: 5px;
    }

    .book-card .rating {
        font-weight: 500; 
        font-size: 0.95rem; 
        text-align: center;
    }

    .book-card .author-year {
        text-align: center; 
        font-size: 0.9rem; 
        color: #444;
    }

    .recommendation-button {
        width: 100%;
    }

    @media (max-width: 768px) {
        .selection-row {
            flex-direction: column;
            align-items: stretch;
        }
    }
</style>

"""