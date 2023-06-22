# Lowering the Threshold for Scientists to Create Linked Open Data: A GitHub Action Approach

### Abstract

This paper explores the use of a GitHub Action (GH-a) to generate a GitHub Pages site from a GitHub repository containing a Research Object Crate (RO-Crate). The paper discusses the motivations behind building this repository, the technologies used, and its significance in lowering the threshold for scientists to create Linked Open Data (LOD) from their research. Additionally, the paper highlights the use of signposting in the generated webpage to make the machine-readable file (ro-crate-metadata.json) discoverable for harvesting.

## Index

* [Introduction](#introduction)
* [Motivation](#motivation)
* [Technologies Used](#technologies-used)
* [Signposting for Discoverability](#signposting-for-discoverability)
* [Significance](#significance)
* [Conclusion](#conclusion)

## Introduction

This paper explores the use of a GitHub Action (GH-a) to generate a GitHub Pages site from a GitHub repository containing a Research Object Crate (RO-Crate). It discusses the motivations, technologies used, and significance of using GH-a to lower the threshold for scientists to create Linked Open Data (LOD) from their research. Additionally, the paper highlights the use of signposting in the generated webpage to make the machine-readable file (ro-crate-metadata.json) easily discoverable for harvesting.

## Motivation

One of the main motivations for making this GH-a is to simplify the process of creating LOD for scientists. The paper highlights the need for a solution that can automate the creation of LOD from research objects. The GH-a is introduced as a solution that addresses this need by providing an automated way to generate a GitHub Pages site from a GitHub repository containing a RO-Crate. This automation simplifies the process for scientists and reduces the technical expertise required.

The GH-a is significant in lowering the threshold for scientists to create LOD. By automating the process, scientists can focus more on their research and less on the technical aspects of creating and publishing LOD. The Action provides a streamlined workflow that generates a GitHub Pages site from a repository containing a RO-Crate. This makes it easier for scientists to share their research data in a machine-readable format, enabling wider access and collaboration.

The GH-a also addresses the need for discoverability of the machine-readable file (ro-crate-metadata.json) for harvesting. The generated webpage uses signposting to make the RO-Crate metadata file discoverable. This ensures that the LOD can be easily found and utilized by others in the research community. The paper emphasizes the importance of discoverability in ensuring the widespread use and reusability of the LOD.

## Technologies Used

The technologies used in building the GitHub Action (GH-a) and the associated GitHub Pages site include:

* YAML configuration files: YAML is a human-readable data serialization format commonly used for configuration files. In this case, YAML files are used to define workflows for the GH-a. Workflows are a series of steps to be executed when certain events occur in a repository.
* GitHub Actions workflows: GitHub Actions is a feature of GitHub that allows you to automate tasks and workflows in your repository. Workflows are defined in YAML files and can be triggered by events such as pushes to the repository.

The advantages of using these technologies include:

* Ease of configuration: YAML configuration files provide a simple and readable syntax for defining workflows, making it easier for developers to understand and modify them as needed.
* Integration with GitHub: GitHub Actions workflows are tightly integrated with the GitHub platform, allowing for seamless integration with other GitHub features such as pull requests and issue tracking.

By utilizing YAML configuration files and GitHub Actions workflows, scientists can automate the process of generating a GitHub Pages site from a GitHub repository containing a Research Object Crate (RO-Crate). This simplifies the process for scientists and reduces the technical expertise required, thereby lowering the threshold for scientists to create Linked Open Data (LOD) from their research.

## Signposting for Discoverability

Signposting in the context of LOD refers to the practice of adding machine-actionable navigation links to make resources discoverable and accessible. In the case of RO-Crate, signposting is used to make the RO-Crate metadata file discoverable for harvesting. This means that the generated webpage includes links and metadata that allow other systems to easily find and consume the RO-Crate metadata.

The generated webpage uses various signposting techniques to enhance discoverability. These techniques include:

Using Web Links (RFC8288) conveyed through HTTP headers or HTML <link> elements to indicate the relationships between the landing page and the downloadable resources, including the RO-Crate metadata file and content resources.
Including persistent identifiers, such as DOIs, for both the research object and its authors. These identifiers serve as globally unique identifiers that can be used to reference the resources.
Leveraging existing standards and vocabularies, such as schema.org, to describe the metadata in a structured and machine-readable format.
Making use of JSON-LD, a format based on RDF principles, to represent the metadata in a linked data format that can be easily consumed by other systems.

The importance of discoverability in LOD cannot be overstated. Discoverability ensures that the resources are easily found, accessed, and reused by both humans and machines. Here are some reasons why discoverability is crucial:

Widespread use: When resources are easily discoverable, they are more likely to be used and cited by other researchers. This promotes collaboration and knowledge sharing within the scientific community.
Reusability: Discoverability allows others to find and reuse the resources, building upon previous work and accelerating scientific progress.
Interoperability: By using signposting techniques and adhering to standards, the generated webpage enhances interoperability with other systems and platforms. This allows for seamless integration and exchange of data between different research tools and environments.
FAIR principles: Discoverability is one of the core principles of FAIR (Findable, Accessible, Interoperable, and Reusable) data. By making resources discoverable, they become more FAIR and align with the best practices for open and accessible data.

In summary, signposting in the context of LOD refers to the practice of adding machine-actionable navigation links to enhance discoverability. In the case of RO-Crate, signposting is used to make the metadata file discoverable for harvesting. Discoverability is crucial for ensuring the widespread use and reusability of LOD, promoting collaboration, and adhering to the FAIR principles.

## Significance

The benefits of lowering the threshold for scientists to create LOD using the GH-a are:

* Increased participation: By simplifying the process and reducing the technical expertise required, more scientists can contribute to the LOD ecosystem. This opens up opportunities for collaboration and knowledge sharing among scientists from different domains.

* Accelerated research: With a lower threshold, scientists can quickly create and share LOD from their research, enabling faster dissemination and discovery of scientific knowledge. This can lead to accelerated research progress and innovation.

* Improved reproducibility: LOD facilitates reproducibility by providing machine-readable metadata and links to related resources. By enabling more scientists to create LOD, the GH-a contributes to improving the reproducibility of scientific research.

## Conclusion

The github-action has the potential to significantly advance scientific research and collaboration by lowering the threshold for scientists to create Linked Open Data. By simplifying the process and providing automation, more scientists can contribute to the Linked Open Data ecosystem, leading to increased collaboration and knowledge sharing in the scientific community.
