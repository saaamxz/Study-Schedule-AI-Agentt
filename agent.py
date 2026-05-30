import os
import pandas as pd

class SimpleAgentExecutor:
    def invoke(self, user_input):
        query = user_input.get("input", "").strip()
        
        if not os.path.exists("schedule.csv"):
            return {"output": "❌ عذراً، ملف الجدول الدراسي schedule.csv غير موجود في مجلد المشروع."}
            
        try:
            # قراءة ملف الجدول الدراسي بالترميز الصحيح للعربي
            df = pd.read_csv("schedule.csv", encoding="utf-8-sig")
            
            # دالة تنظيف النصوص لتفادي مشاكل الهمزات والتاء المربوطة في البحث
            def clean_text(text):
                if not isinstance(text, str): return ""
                return text.replace("أ", "ا").replace("إ", "ا").replace("ة", "ه").strip().lower()
            
            query_clean = clean_text(query)
            
            # تحديد القسم المذكور في السؤال (CS, IS, AI, SE)
            selected_dept = None
            for dept in ['cs', 'is', 'ai', 'se']:
                if dept in query_clean:
                    selected_dept = dept.upper()
                    break
            
            # تحديد اليوم المذكور في السؤال
            days_list = ['السبت', 'الاحد', 'الاثنين', 'الثلاثاء', 'الاربعاء', 'الخميس']
            selected_day = None
            for day in days_list:
                if clean_text(day) in query_clean:
                    selected_day = day
                    break
            
            # فلترة الجدول بناءً على القسم واليوم اللي المستخدم كتبهم
            filtered_df = df.copy()
            if selected_dept:
                filtered_df = filtered_df[filtered_df['department'].str.upper() == selected_dept]
            if selected_day:
                filtered_df = filtered_df[filtered_df['day'].apply(clean_text) == clean_text(selected_day)]
                
            if filtered_df.empty:
                return {"output": f"🔍 لم أجد محاضرات أو سكاشن مطابقة لطلبك في الجدول الدراسي بناءً على بحثك عن ({query})."}
            
            # تنسيق الإجابة بشكل جمالي ومنظم جداً ومنسق بالنقاط
            output = f"### 📅 الجدول الدراسي المستخرج بنجاح:\n\n"
            for idx, row in filtered_df.iterrows():
                output += f"* **المادة:** {row['subject']} ({row['type']})\n"
                output += f"  * **القسم:** {row['department']} | **السكشن/المجموعة:** {row['section']}\n"
                output += f"  * **الموعد:** من {row['time_from']} إلى {row['time_to']} (يوم {row['day']})\n"
                output += f"  * **المحاضر:** {row['instructor']}\n"
                output += f"  * **المكان:** {row['location']}\n"
                output += f"  --------------------------------------------------\n"
            return {"output": output}
            
        except Exception as e:
            return {"output": f"❌ حدث خطأ داخلي أثناء معالجة البيانات: {str(e)}"}

# تصدير المحرك ليعمل مع ملف app.py مباشرة وبدون تعديل
agent_executor = SimpleAgentExecutor()