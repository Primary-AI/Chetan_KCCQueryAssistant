# 📊 Sample Queries for KCC Query Assistant

Below are 10+ real-world sample queries tested using the KCC Query Assistant.

---

### 🌾 Crop Protection & Pest Control

1. **What is the pest control method for redgram affected by pod borer in Bellary district?**  
→ ✅ Answer retrieved from KCC dataset

2. **How to manage powdery mildew in grapes?**  
→ ✅ Answer retrieved from KCC dataset

3. **What pesticide to use for whitefly in cotton crops?**  
→ ✅ Retrieved from LLM / KCC

---

### 🌱 Fertilizer & Soil

4. **What is the recommended fertilizer dose for tomato in Tumkur?**  
→ ✅ Answer retrieved from KCC

5. **Which fertilizer to use for paddy in Karnataka?**  
→ ✅ KCC + LLM fallback tested

---

### 💧 Water Stress & Drought

6. **How to handle drought stress in sugarcane?**  
→ ✅ Triggered fallback LLM and DuckDuckGo live search

7. **Water-saving techniques in groundnut farming**  
→ ✅ Answer retrieved from KCC dataset

---

### 🌐 Policy & General Info

8. **What is the agriculture export policy of India?**  
→ ✅ No match in KCC, answered via LLM + DuckDuckGo

9. **What government schemes are available for organic farming in Karnataka?**  
→ ✅ Retrieved via fallback internet search

---

### 🧪 Miscellaneous / Invalid Queries

10. **King**  
→ ⚠️ No match — vague query handled gracefully, fallback engaged

11. **Dog**  
→ ⚠️ No match in KCC — handled with informative LLM response, fallback triggered

---

✅ These queries demonstrate the complete flow:
- KCC semantic retrieval
- LLM fallback when no match
- Internet live search (DuckDuckGo)
