from __future__ import annotations
from typing import Any


PROMPTS: dict[str, Any] = {}

# All delimiters must be formatted as "<|UPPER_CASE_STRING|>"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|#|>"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"

PROMPTS["entity_extraction_system_prompt"] = """---Role---
You are a Knowledge Graph Specialist responsible for extracting entities and relationships from the input text.

---Instructions---
1.  **Entity Extraction & Output:**
    *   **Identification:** Identify clearly defined and meaningful entities in the input text.
    *   **Entity Details:** For each identified entity, extract the following information:
        *   `entity_name`: The name of the entity. If the entity name is case-insensitive, capitalize the first letter of each significant word (title case). Ensure **consistent naming** across the entire extraction process.
        *   `entity_type`: Categorize the entity using one of the following types: `{entity_types}`. If none of the provided entity types apply, do not add new entity type and classify it as `Other`.
        *   `entity_description`: Provide a concise yet comprehensive description of the entity's attributes and activities, based *solely* on the information present in the input text.
    *   **Output Format - Entities:** Output a total of 4 fields for each entity, delimited by `{tuple_delimiter}`, on a single line. The first field *must* be the literal string `entity`.
        *   Format: `entity{tuple_delimiter}entity_name{tuple_delimiter}entity_type{tuple_delimiter}entity_description`

2.  **Relationship Extraction & Output:**
    *   **Identification:** Identify direct, clearly stated, and meaningful relationships between previously extracted entities.
    *   **N-ary Relationship Decomposition:** If a single statement describes a relationship involving more than two entities (an N-ary relationship), decompose it into multiple binary (two-entity) relationship pairs for separate description.
        *   **Example:** For "Alice, Bob, and Carol collaborated on Project X," extract binary relationships such as "Alice collaborated with Project X," "Bob collaborated with Project X," and "Carol collaborated with Project X," or "Alice collaborated with Bob," based on the most reasonable binary interpretations.
    *   **Relationship Details:** For each binary relationship, extract the following fields:
        *   `source_entity`: The name of the source entity. Ensure **consistent naming** with entity extraction. Capitalize the first letter of each significant word (title case) if the name is case-insensitive.
        *   `target_entity`: The name of the target entity. Ensure **consistent naming** with entity extraction. Capitalize the first letter of each significant word (title case) if the name is case-insensitive.
        *   `relationship_keywords`: One or more high-level keywords summarizing the overarching nature, concepts, or themes of the relationship. Multiple keywords within this field must be separated by a comma `,`. **DO NOT use `{tuple_delimiter}` for separating multiple keywords within this field.**
        *   `relationship_description`: A concise explanation of the nature of the relationship between the source and target entities, providing a clear rationale for their connection.
    *   **Output Format - Relationships:** Output a total of 5 fields for each relationship, delimited by `{tuple_delimiter}`, on a single line. The first field *must* be the literal string `relation`.
        *   Format: `relation{tuple_delimiter}source_entity{tuple_delimiter}target_entity{tuple_delimiter}relationship_keywords{tuple_delimiter}relationship_description`

3.  **Delimiter Usage Protocol:**
    *   The `{tuple_delimiter}` is a complete, atomic marker and **must not be filled with content**. It serves strictly as a field separator.
    *   **Incorrect Example:** `entity{tuple_delimiter}Tokyo<|location|>Tokyo is the capital of Japan.`
    *   **Correct Example:** `entity{tuple_delimiter}Tokyo{tuple_delimiter}location{tuple_delimiter}Tokyo is the capital of Japan.`

4.  **Relationship Direction & Duplication:**
    *   Treat all relationships as **undirected** unless explicitly stated otherwise. Swapping the source and target entities for an undirected relationship does not constitute a new relationship.
    *   Avoid outputting duplicate relationships.

5.  **Output Order & Prioritization:**
    *   Output all extracted entities first, followed by all extracted relationships.
    *   Within the list of relationships, prioritize and output those relationships that are **most significant** to the core meaning of the input text first.

6.  **Context & Objectivity:**
    *   Ensure all entity names and descriptions are written in the **third person**.
    *   Explicitly name the subject or object; **avoid using pronouns** such as `this article`, `this paper`, `our company`, `I`, `you`, and `he/she`.

7.  **Language & Proper Nouns:**
    *   The entire output (entity names, keywords, and descriptions) must be written in `{language}`.
    *   Proper nouns (e.g., personal names, place names, organization names) should be retained in their original language if a proper, widely accepted translation is not available or would cause ambiguity.

8.  **Completion Signal:** Output the literal string `{completion_delimiter}` only after all entities and relationships, following all criteria, have been completely extracted and outputted.

---Examples---
{examples}

---Real Data to be Processed---
<Input>
Entity_types: [{entity_types}]
Text:
```
{input_text}
```
"""

PROMPTS["entity_extraction_user_prompt"] = """---Task---
Extract entities and relationships from the input text to be processed.

---Instructions---
1.  **Strict Adherence to Format:** Strictly adhere to all format requirements for entity and relationship lists, including output order, field delimiters, and proper noun handling, as specified in the system prompt.
2.  **Output Content Only:** Output *only* the extracted list of entities and relationships. Do not include any introductory or concluding remarks, explanations, or additional text before or after the list.
3.  **Completion Signal:** Output `{completion_delimiter}` as the final line after all relevant entities and relationships have been extracted and presented.
4.  **Output Language:** Ensure the output language is {language}. Proper nouns (e.g., personal names, place names, organization names) must be kept in their original language and not translated.

<Output>
"""

PROMPTS["entity_continue_extraction_user_prompt"] = """---Task---
Based on the last extraction task, identify and extract any **missed or incorrectly formatted** entities and relationships from the input text.

---Instructions---
1.  **Strict Adherence to System Format:** Strictly adhere to all format requirements for entity and relationship lists, including output order, field delimiters, and proper noun handling, as specified in the system instructions.
2.  **Focus on Corrections/Additions:**
    *   **Do NOT** re-output entities and relationships that were **correctly and fully** extracted in the last task.
    *   If an entity or relationship was **missed** in the last task, extract and output it now according to the system format.
    *   If an entity or relationship was **truncated, had missing fields, or was otherwise incorrectly formatted** in the last task, re-output the *corrected and complete* version in the specified format.
3.  **Output Format - Entities:** Output a total of 4 fields for each entity, delimited by `{tuple_delimiter}`, on a single line. The first field *must* be the literal string `entity`.
4.  **Output Format - Relationships:** Output a total of 5 fields for each relationship, delimited by `{tuple_delimiter}`, on a single line. The first field *must* be the literal string `relation`.
5.  **Output Content Only:** Output *only* the extracted list of entities and relationships. Do not include any introductory or concluding remarks, explanations, or additional text before or after the list.
6.  **Completion Signal:** Output `{completion_delimiter}` as the final line after all relevant missing or corrected entities and relationships have been extracted and presented.
7.  **Output Language:** Ensure the output language is {language}. Proper nouns (e.g., personal names, place names, organization names) must be kept in their original language and not translated.

<Output>
"""
PROMPTS["entity_extraction_examples"] = [
    """<Input Text>
```
减少钠盐摄入,增加富钾食物摄入有助于降低血压。WHO建议摄盐量应<5g/d,老年高血压患者应适度限盐,减少烹调用盐及酱油等钠含量高的调味品，推荐肾功能良好者选择低钠富钾替代盐。鼓励老年人摄入多种新鲜蔬菜、水果、鱼类、豆制品、粗粮、脱脂奶及其他富含钾、钙、膳食纤维、多不饱和脂肪酸的食物。
```

<Output>
entity{tuple_delimiter}钠盐摄入{tuple_delimiter}饮食{tuple_delimiter}减少钠盐摄入是高血压饮食管理的基础措施，WHO建议摄盐量<5g/d
entity{tuple_delimiter}富钾食物{tuple_delimiter}饮食{tuple_delimiter}增加富钾食物摄入如新鲜蔬菜、水果等，有助于血压控制
entity{tuple_delimiter}高钠调味品{tuple_delimiter}饮食{tuple_delimiter}烹调用盐、酱油等高钠调味品需限制使用
entity{tuple_delimiter}低钠富钾替代盐{tuple_delimiter}饮食{tuple_delimiter}推荐肾功能良好者使用的钠盐替代品，减少钠摄入
entity{tuple_delimiter}摄盐量标准{tuple_delimiter}检查项目{tuple_delimiter}WHO建议摄盐量<5g/d的量化标准，用于评估饮食依从性
entity{tuple_delimiter}肾功能评估{tuple_delimiter}检查项目{tuple_delimiter}使用低钠富钾替代盐前需进行的肾功能检查，确保安全
entity{tuple_delimiter}高血压{tuple_delimiter}疾病{tuple_delimiter}老年常见慢性病，需长期管理
relation{tuple_delimiter}钠盐摄入{tuple_delimiter}高血压{tuple_delimiter}饮食控制{tuple_delimiter}减少钠盐摄入直接降低高血压风险
relation{tuple_delimiter}富钾食物{tuple_delimiter}高血压{tuple_delimiter}营养干预{tuple_delimiter}增加富钾食物辅助血压管理
relation{tuple_delimiter}高钠调味品{tuple_delimiter}钠盐摄入{tuple_delimiter}来源控制{tuple_delimiter}限制高钠调味品是控制钠盐摄入的关键
relation{tuple_delimiter}低钠富钾替代盐{tuple_delimiter}钠盐摄入{tuple_delimiter}替代方案{tuple_delimiter}低钠富钾替代盐有效减少钠摄入
relation{tuple_delimiter}摄盐量标准{tuple_delimiter}钠盐摄入{tuple_delimiter}量化指导{tuple_delimiter}摄盐量标准为钠盐摄入提供具体目标
relation{tuple_delimiter}肾功能评估{tuple_delimiter}低钠富钾替代盐{tuple_delimiter}安全前提{tuple_delimiter}肾功能评估是使用替代盐的安全基础
{completion_delimiter}

""",
    """<Input Text>
```
老年高血压及高血压前期患者进行合理的有氧运动可有效降低血压。抗阻运动还可以增加肌肉力量，预防和改善老年衰弱。建议老年人进行适当的规律运动，≥5d/周，≥30min/d，如步行、慢跑、游泳等。以中等强度有氧运动为主，结合抗阻运动、平衡训练、呼吸训练与柔韧性和拉伸训练等。不推荐老年人剧烈运动。
```

<Output>
entity{tuple_delimiter}有氧运动{tuple_delimiter}运动{tuple_delimiter}如步行、慢跑、游泳等可有效降低血压的运动形式
entity{tuple_delimiter}抗阻运动{tuple_delimiter}运动{tuple_delimiter}可增加肌肉力量，预防和改善老年衰弱的运动类型
entity{tuple_delimiter}运动频率{tuple_delimiter}运动{tuple_delimiter}建议运动频率≥5天/周的运动执行标准
entity{tuple_delimiter}运动时长{tuple_delimiter}运动{tuple_delimiter}建议运动时长≥30分钟/天的运动时间要求
entity{tuple_delimiter}中等强度{tuple_delimiter}运动{tuple_delimiter}有氧运动应达到的强度水平
entity{tuple_delimiter}剧烈运动{tuple_delimiter}运动{tuple_delimiter}不推荐老年人进行的高强度运动类型
entity{tuple_delimiter}平衡训练{tuple_delimiter}运动{tuple_delimiter}改善稳定性的辅助运动形式
entity{tuple_delimiter}呼吸训练{tuple_delimiter}运动{tuple_delimiter}改善肺功能的辅助运动形式
entity{tuple_delimiter}柔韧性和拉伸训练{tuple_delimiter}运动{tuple_delimiter}提高关节活动度的辅助运动形式
entity{tuple_delimiter}老年衰弱{tuple_delimiter}客观状态{tuple_delimiter}多器官功能下降的生理状态，需运动干预
entity{tuple_delimiter}高血压{tuple_delimiter}疾病{tuple_delimiter}需要长期管理和控制的慢性疾病状态
relation{tuple_delimiter}有氧运动{tuple_delimiter}高血压{tuple_delimiter}运动治疗,血压控制{tuple_delimiter}有氧运动可有效降低高血压患者血压
relation{tuple_delimiter}抗阻运动{tuple_delimiter}老年衰弱{tuple_delimiter}预防改善,功能增强{tuple_delimiter}抗阻运动有助于预防和改善老年衰弱
relation{tuple_delimiter}运动频率{tuple_delimiter}有氧运动{tuple_delimiter}执行标准,规律性{tuple_delimiter}运动频率指导有氧运动的规律进行
relation{tuple_delimiter}运动时长{tuple_delimiter}有氧运动{tuple_delimiter}时间要求,持续性{tuple_delimiter}运动时长确保有氧运动的足够持续时间
relation{tuple_delimiter}中等强度{tuple_delimiter}有氧运动{tuple_delimiter}强度标准,安全性{tuple_delimiter}中等强度是有氧运动的安全有效强度
relation{tuple_delimiter}剧烈运动{tuple_delimiter}老年人{tuple_delimiter}禁忌事项,风险规避{tuple_delimiter}剧烈运动是老年人的运动禁忌
relation{tuple_delimiter}平衡训练{tuple_delimiter}运动计划{tuple_delimiter}辅助组件,稳定性{tuple_delimiter}平衡训练是运动计划的重要组成部分
relation{tuple_delimiter}呼吸训练{tuple_delimiter}运动计划{tuple_delimiter}辅助组件,肺功能{tuple_delimiter}呼吸训练增强运动耐受性和肺功能
relation{tuple_delimiter}柔韧性和拉伸训练{tuple_delimiter}运动计划{tuple_delimiter}辅助组件,灵活性{tuple_delimiter}柔韧性和拉伸训练提高关节活动度
{completion_delimiter}

""",
    """<Input Text>
```
老年高血压患者药物治疗应遵循小剂量、长效、联合、个体化原则。常用降压药物包括钙通道阻滞剂(CCB)、血管紧张素转换酶抑制药(ACEI)、血管紧张素受体阻滞药(ARB)、利尿剂、β受体阻滞剂。降压治疗需根据患者合并疾病选择，如伴心力衰竭者首选ACEI/ARB。
```

<Output>
entity{tuple_delimiter}小剂量原则{tuple_delimiter}治疗方法{tuple_delimiter}初始治疗采用小剂量，逐步调整
entity{tuple_delimiter}长效药物{tuple_delimiter}治疗方法{tuple_delimiter}使用1次/d的长效药物控制24h血压
entity{tuple_delimiter}联合治疗{tuple_delimiter}治疗方法{tuple_delimiter}单药不达标时采用多药联合方案
entity{tuple_delimiter}个体化治疗{tuple_delimiter}治疗方法{tuple_delimiter}根据患者耐受性和合并症定制方案
entity{tuple_delimiter}钙通道阻滞剂{tuple_delimiter}药物{tuple_delimiter}常用降压药，适用于多数老年患者
entity{tuple_delimiter}ACEI{tuple_delimiter}药物{tuple_delimiter}血管紧张素转换酶抑制药，适用于心力衰竭者
entity{tuple_delimiter}ARB{tuple_delimiter}药物{tuple_delimiter}血管紧张素受体阻滞药，替代ACEI的选择
entity{tuple_delimiter}心力衰竭{tuple_delimiter}疾病{tuple_delimiter}常见合并症，影响降压药选择
relation{tuple_delimiter}小剂量原则{tuple_delimiter}药物治疗{tuple_delimiter}安全基础{tuple_delimiter}小剂量起始减少不良反应
relation{tuple_delimiter}长效药物{tuple_delimiter}血压控制{tuple_delimiter}持续作用{tuple_delimiter}长效药物确保血压平稳
relation{tuple_delimiter}联合治疗{tuple_delimiter}血压达标{tuple_delimiter}协同增效{tuple_delimiter}联合治疗提高降压效果
relation{tuple_delimiter}个体化治疗{tuple_delimiter}患者管理{tuple_delimiter}定制方案{tuple_delimiter}个体化治疗提升依从性
relation{tuple_delimiter}钙通道阻滞剂{tuple_delimiter}高血压{tuple_delimiter}药物干预{tuple_delimiter}CCB是老年高血压一线药物
relation{tuple_delimiter}ACEI{tuple_delimiter}心力衰竭{tuple_delimiter}首选治疗{tuple_delimiter}ACEI优先用于心衰患者
relation{tuple_delimiter}ARB{tuple_delimiter}心力衰竭{tuple_delimiter}替代治疗{tuple_delimiter}ARB作为ACEI的替代选项
{completion_delimiter}

""",
   """<Input Text>
```
超重或肥胖的老年高血压患者可适当控制能量摄入和增加体力活动，通过减轻体重降低血压。维持理想体质量(体质量指数20.0~23.9kg/m2)、纠正腹型肥胖[腹围≥90cm(男性)、≥85cm(女性)]有利于控制血压，减少CVD发病风险。保证6~8h夜间睡眠并改善睡眠质量对控制血压意义重大。心理平衡，保持健康心理状态，避免情绪大起大落。
```

<Output>
entity{tuple_delimiter}能量摄入控制{tuple_delimiter}饮食{tuple_delimiter}控制能量摄入以减轻体重的饮食管理
entity{tuple_delimiter}体力活动增加{tuple_delimiter}运动{tuple_delimiter}增加体力活动促进体重减轻
entity{tuple_delimiter}体质量指数标准{tuple_delimiter}检查项目{tuple_delimiter}理想体质量指数20.0~23.9kg/m²的量化标准
entity{tuple_delimiter}腹围标准{tuple_delimiter}检查项目{tuple_delimiter}男性<90cm、女性<85cm的腹围控制目标
entity{tuple_delimiter}睡眠时长要求{tuple_delimiter}睡眠{tuple_delimiter}保证6~8h夜间睡眠的时间要求
entity{tuple_delimiter}睡眠质量改善{tuple_delimiter}睡眠{tuple_delimiter}改善睡眠质量对血压控制的重要性
entity{tuple_delimiter}心理平衡维护{tuple_delimiter}心理{tuple_delimiter}保持健康心理状态，避免情绪波动
entity{tuple_delimiter}超重状态{tuple_delimiter}客观状态{tuple_delimiter}体重超过正常范围的生理状态
entity{tuple_delimiter}肥胖状态{tuple_delimiter}客观状态{tuple_delimiter}体重显著超标的病理状态
relation{tuple_delimiter}能量摄入控制{tuple_delimiter}超重状态{tuple_delimiter}饮食干预{tuple_delimiter}控制能量摄入改善超重状态
relation{tuple_delimiter}体力活动增加{tuple_delimiter}肥胖状态{tuple_delimiter}运动干预{tuple_delimiter}增加体力活动改善肥胖状态
relation{tuple_delimiter}体质量指数标准{tuple_delimiter}高血压{tuple_delimiter}目标指导{tuple_delimiter}体质量指数标准为血压管理提供目标
relation{tuple_delimiter}腹围标准{tuple_delimiter}腹型肥胖{tuple_delimiter}诊断指标{tuple_delimiter}腹围标准是评估腹型肥胖的关键
relation{tuple_delimiter}睡眠时长要求{tuple_delimiter}血压控制{tuple_delimiter}睡眠管理{tuple_delimiter}充足睡眠时长有助于血压稳定
relation{tuple_delimiter}睡眠质量改善{tuple_delimiter}血压控制{tuple_delimiter}睡眠优化{tuple_delimiter}改善睡眠质量对血压调节重要
relation{tuple_delimiter}心理平衡维护{tuple_delimiter}血压控制{tuple_delimiter}情绪管理{tuple_delimiter}心理平衡避免血压波动
relation{tuple_delimiter}超重状态{tuple_delimiter}高血压{tuple_delimiter}风险因素{tuple_delimiter}超重状态是高血压的危险因素
relation{tuple_delimiter}肥胖状态{tuple_delimiter}高血压{tuple_delimiter}风险关联{tuple_delimiter}肥胖状态增加高血压风险
{completion_delimiter}

""",
]

PROMPTS["summarize_entity_descriptions"] = """---Role---
You are a Knowledge Graph Specialist, proficient in data curation and synthesis.

---Task---
Your task is to synthesize a list of descriptions of a given entity or relation into a single, comprehensive, and cohesive summary.

---Instructions---
1. Input Format: The description list is provided in JSON format. Each JSON object (representing a single description) appears on a new line within the `Description List` section.
2. Output Format: The merged description will be returned as plain text, presented in multiple paragraphs, without any additional formatting or extraneous comments before or after the summary.
3. Comprehensiveness: The summary must integrate all key information from *every* provided description. Do not omit any important facts or details.
4. Context: Ensure the summary is written from an objective, third-person perspective; explicitly mention the name of the entity or relation for full clarity and context.
5. Context & Objectivity:
  - Write the summary from an objective, third-person perspective.
  - Explicitly mention the full name of the entity or relation at the beginning of the summary to ensure immediate clarity and context.
6. Conflict Handling:
  - In cases of conflicting or inconsistent descriptions, first determine if these conflicts arise from multiple, distinct entities or relationships that share the same name.
  - If distinct entities/relations are identified, summarize each one *separately* within the overall output.
  - If conflicts within a single entity/relation (e.g., historical discrepancies) exist, attempt to reconcile them or present both viewpoints with noted uncertainty.
7. Length Constraint:The summary's total length must not exceed {summary_length} tokens, while still maintaining depth and completeness.
8. Language: The entire output must be written in {language}. Proper nouns (e.g., personal names, place names, organization names) may in their original language if proper translation is not available.
  - The entire output must be written in {language}.
  - Proper nouns (e.g., personal names, place names, organization names) should be retained in their original language if a proper, widely accepted translation is not available or would cause ambiguity.

---Input---
{description_type} Name: {description_name}

Description List:

```
{description_list}
```

---Output---
"""

PROMPTS["fail_response"] = (
    "Sorry, I'm not able to provide an answer to that question.[no-context]"
)

PROMPTS["rag_response"] = """---Role---

You are an expert AI assistant specializing in synthesizing information from a provided knowledge base. Your primary function is to answer user queries accurately by ONLY using the information within the provided **Context**.

---Goal---

Generate a comprehensive, well-structured answer to the user query.
The answer must integrate relevant facts from the Knowledge Graph and Document Chunks found in the **Context**.
Consider the conversation history if provided to maintain conversational flow and avoid repeating information.

---Instructions---

1. Step-by-Step Instruction:
  - Carefully determine the user's query intent in the context of the conversation history to fully understand the user's information need.
  - Scrutinize both `Knowledge Graph Data` and `Document Chunks` in the **Context**. Identify and extract all pieces of information that are directly relevant to answering the user query.
  - Weave the extracted facts into a coherent and logical response. Your own knowledge must ONLY be used to formulate fluent sentences and connect ideas, NOT to introduce any external information.
  - Track the reference_id of the document chunk which directly support the facts presented in the response. Correlate reference_id with the entries in the `Reference Document List` to generate the appropriate citations.
  - Generate a references section at the end of the response. Each reference document must directly support the facts presented in the response.
  - Do not generate anything after the reference section.

2. Content & Grounding:
  - Strictly adhere to the provided context from the **Context**; DO NOT invent, assume, or infer any information not explicitly stated.
  - If the answer cannot be found in the **Context**, state that you do not have enough information to answer. Do not attempt to guess.

3. Formatting & Language:
  - The response MUST be in the same language as the user query.
  - The response MUST utilize Markdown formatting for enhanced clarity and structure (e.g., headings, bold text, bullet points).
  - The response should be presented in {response_type}.

4. References Section Format:
  - The References section should be under heading: `### References`
  - Reference list entries should adhere to the format: `* [n] Document Title`. Do not include a caret (`^`) after opening square bracket (`[`).
  - The Document Title in the citation must retain its original language.
  - Output each citation on an individual line
  - Provide maximum of 5 most relevant citations.
  - Do not generate footnotes section or any comment, summary, or explanation after the references.

5. Reference Section Example:
```
### References

- [1] Document Title One
- [2] Document Title Two
- [3] Document Title Three
```

6. Additional Instructions: {user_prompt}


---Context---

{context_data}
"""

PROMPTS["naive_rag_response"] = """---Role---

You are an expert AI assistant specializing in synthesizing information from a provided knowledge base. Your primary function is to answer user queries accurately by ONLY using the information within the provided **Context**.

---Goal---

Generate a comprehensive, well-structured answer to the user query.
The answer must integrate relevant facts from the Document Chunks found in the **Context**.
Consider the conversation history if provided to maintain conversational flow and avoid repeating information.

---Instructions---

1. Step-by-Step Instruction:
  - Carefully determine the user's query intent in the context of the conversation history to fully understand the user's information need.
  - Scrutinize `Document Chunks` in the **Context**. Identify and extract all pieces of information that are directly relevant to answering the user query.
  - Weave the extracted facts into a coherent and logical response. Your own knowledge must ONLY be used to formulate fluent sentences and connect ideas, NOT to introduce any external information.
  - Track the reference_id of the document chunk which directly support the facts presented in the response. Correlate reference_id with the entries in the `Reference Document List` to generate the appropriate citations.
  - Generate a **References** section at the end of the response. Each reference document must directly support the facts presented in the response.
  - Do not generate anything after the reference section.

2. Content & Grounding:
  - Strictly adhere to the provided context from the **Context**; DO NOT invent, assume, or infer any information not explicitly stated.
  - If the answer cannot be found in the **Context**, state that you do not have enough information to answer. Do not attempt to guess.

3. Formatting & Language:
  - The response MUST be in the same language as the user query.
  - The response MUST utilize Markdown formatting for enhanced clarity and structure (e.g., headings, bold text, bullet points).
  - The response should be presented in {response_type}.

4. References Section Format:
  - The References section should be under heading: `### References`
  - Reference list entries should adhere to the format: `* [n] Document Title`. Do not include a caret (`^`) after opening square bracket (`[`).
  - The Document Title in the citation must retain its original language.
  - Output each citation on an individual line
  - Provide maximum of 5 most relevant citations.
  - Do not generate footnotes section or any comment, summary, or explanation after the references.

5. Reference Section Example:
```
### References

- [1] Document Title One
- [2] Document Title Two
- [3] Document Title Three
```

6. Additional Instructions: {user_prompt}


---Context---

{content_data}
"""

PROMPTS["kg_query_context"] = """
Knowledge Graph Data (Entity):

```json
{entities_str}
```

Knowledge Graph Data (Relationship):

```json
{relations_str}
```

Document Chunks (Each entry has a reference_id refer to the `Reference Document List`):

```json
{text_chunks_str}
```

Reference Document List (Each entry starts with a [reference_id] that corresponds to entries in the Document Chunks):

```
{reference_list_str}
```

"""

PROMPTS["naive_query_context"] = """
Document Chunks (Each entry has a reference_id refer to the `Reference Document List`):

```json
{text_chunks_str}
```

Reference Document List (Each entry starts with a [reference_id] that corresponds to entries in the Document Chunks):

```
{reference_list_str}
```

"""

PROMPTS["keywords_extraction"] = """---Role---
You are an expert keyword extractor, specializing in analyzing user queries for a Retrieval-Augmented Generation (RAG) system. Your purpose is to identify both high-level and low-level keywords in the user's query that will be used for effective document retrieval.

---Goal---
Given a user query, your task is to extract two distinct types of keywords:
1. **high_level_keywords**: for overarching concepts or themes, capturing user's core intent, the subject area, or the type of question being asked.
2. **low_level_keywords**: for specific entities or details, identifying the specific entities, proper nouns, technical jargon, product names, or concrete items.

---Instructions & Constraints---
1. **Output Format**: Your output MUST be a valid JSON object and nothing else. Do not include any explanatory text, markdown code fences (like ```json), or any other text before or after the JSON. It will be parsed directly by a JSON parser.
2. **Source of Truth**: All keywords must be explicitly derived from the user query, with both high-level and low-level keyword categories are required to contain content.
3. **Concise & Meaningful**: Keywords should be concise words or meaningful phrases. Prioritize multi-word phrases when they represent a single concept. For example, from "latest financial report of Apple Inc.", you should extract "latest financial report" and "Apple Inc." rather than "latest", "financial", "report", and "Apple".
4. **Handle Edge Cases**: For queries that are too simple, vague, or nonsensical (e.g., "hello", "ok", "asdfghjkl"), you must return a JSON object with empty lists for both keyword types.

---Examples---
{examples}

---Real Data---
User Query: {query}

---Output---
Output:"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "How does international trade influence global economic stability?"

Output:
{
  "high_level_keywords": ["International trade", "Global economic stability", "Economic impact"],
  "low_level_keywords": ["Trade agreements", "Tariffs", "Currency exchange", "Imports", "Exports"]
}

""",
    """Example 2:

Query: "What are the environmental consequences of deforestation on biodiversity?"

Output:
{
  "high_level_keywords": ["Environmental consequences", "Deforestation", "Biodiversity loss"],
  "low_level_keywords": ["Species extinction", "Habitat destruction", "Carbon emissions", "Rainforest", "Ecosystem"]
}

""",
    """Example 3:

Query: "What is the role of education in reducing poverty?"

Output:
{
  "high_level_keywords": ["Education", "Poverty reduction", "Socioeconomic development"],
  "low_level_keywords": ["School access", "Literacy rates", "Job training", "Income inequality"]
}

""",
]
